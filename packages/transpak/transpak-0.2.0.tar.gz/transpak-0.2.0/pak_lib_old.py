import os
import time
import json
import struct
import numpy as np
import mkl_fft

import zlib
import bz2
import lzma


# Helper Class to serially unpack data:
# =====================================


class bindata:
    def __init__(self, data, initial_position=0):
        self.pointer = initial_position
        self.data = data

    def read(self, format_chars):
        is_one_value = len(format_chars) == 1
        size = struct.calcsize(format_chars)
        if format_chars[0] != "=":
            format_chars = "=" + format_chars
        values = struct.unpack(
            format_chars, self.data[self.pointer : self.pointer + size]
        )
        self.pointer += size
        if is_one_value:
            return values[0]
        return values

    def read_rest(self, format_char):
        format_size = struct.calcsize(format_chars)
        remaining_data_size = len(self.data) - self.pointer
        if remaining_data_size % format_size != 0:
            print(
                "WARNING: format_char does not align with remaining data in read_rest"
            )
        computed_format_chars = remaining_data_size // format_size
        return read(computed_format_chars)

    def read_raw(self, no_of_bytes=1):
        raw_bytes = self.data[self.pointer : self.pointer + no_of_bytes]
        self.pointer += no_of_bytes
        return raw_bytes

    def read_rest_raw(self):
        return self.data[self.pointer :]

    def reset_pointer(self, pos=0):
        self.pointer = pos


# def decompress(data, lib=bz2):
#     return np.frombuffer(lib.decompress(data), dtype=np.float16)


# Pack Functions:
# ===============


def pack_data(data_list, samplerate):
    versions = []
    data_lengths = []
    data_paks = []
    for data in data_list:
        paksizes = []
        paks_temp = []
        for ver in (1, 2, 3, 4):
            # for ver in (1,2):
            pak = pack_wave(ver, data, samplerate)
            pak_compressed = zlib.compress(pak)
            paks_temp.append(pak_compressed)
            paksizes.append(len(pak_compressed))
        best_version_index = paksizes.index(min(paksizes))
        data_lengths.append(min(paksizes))
        data_paks.append(paks_temp[best_version_index])
        versions.append((1, 2, 3, 4)[best_version_index])
    return versions, data_lengths, data_paks


def pack_wave(version, data, samplerate):
    if version == 1:
        pack = struct.pack(f"{len(data)}f", *data)
    elif version == 2:
        diff_data = np.diff(data)
        pack = struct.pack(f"{len(data)}f", data[0], *diff_data)
    elif version == 3 or version == 4:
        num_components = 30
        freqs, amps, phases = cos_components(data, num_components=num_components)
        pack = struct.pack(f"{num_components}f", *freqs)
        pack += struct.pack(f"{num_components}f", *amps)
        pack += struct.pack(f"{num_components}f", *phases)
        u_recr = recreate_from_components(freqs, amps, phases, samplerate, data.size)
        res = data - u_recr
        if version == 3:
            pack += struct.pack(f"{len(data)}f", *res)
        if version == 4:
            pack += struct.pack(f"{len(data)}f", res[0], *np.diff(res))
    return pack


def calc_affected_channels_code(affected_channels):
    affected_channels_code = 0
    for i in [0, 1, 2, 3, 4, 5, 6, 7]:
        if i in affected_channels:
            affected_channels_code += 2 ** i
    return affected_channels_code


def pack(
    data_list,
    ms_timestamp,
    samplerate,
    maxvoltage=0,
    maxdeviation=0,
    affected_channels=[],
):
    PAK_VERSION = 1
    pack = struct.pack("H", int(PAK_VERSION))
    pack += struct.pack("Q", int(ms_timestamp))
    pack += struct.pack("I", int(samplerate))
    pack += struct.pack("I", data_list[0].size)
    pack += struct.pack("d", maxvoltage)
    pack += struct.pack("d", maxdeviation)
    pack += struct.pack("H", calc_affected_channels_code(affected_channels))

    versions, data_lengths, data_paks = pack_data(data_list, samplerate)
    pack += struct.pack("8I", *data_lengths)
    pack += struct.pack("8H", *versions)

    for data_pak in data_paks:
        pack += data_pak

    return pack


def pack_simple(
    data_list,
    ms_timestamp,
    samplerate,
    maxvoltage=0,
    maxdeviation=0,
    affected_channels=[],
):
    PAK_VERSION = 2
    pack = struct.pack("H", int(PAK_VERSION))
    pack += struct.pack("Q", int(ms_timestamp))
    pack += struct.pack("I", int(samplerate))
    pack += struct.pack("I", data_list[0].size)
    pack += struct.pack("d", maxvoltage)
    pack += struct.pack("d", maxdeviation)
    pack += struct.pack("H", 255)

    versions, data_lengths, data_paks = pack_data(data_list, samplerate)
    pack += struct.pack("8I", *[d.size for d in data_list])
    pack += struct.pack("8H", *(2, 2, 2, 2, 2, 2, 2, 2))

    for data in data_list:
        data_pack = struct.pack(f"{len(data)}f", data[0], *np.diff(data))
        pack += data_pack

    pack = zlib.compress(pack)

    return pack


# Unpack Functions:
# =================


def unpack_file(filepath):
    with open(filepath, "rb") as f:
        data_list, metadata = unpack(f.read())
    return data_list, metadata


def unpack(packed_data, only_metadata=False):

    data = bindata(packed_data)
    pak_version = data.read("H")

    if pak_version == 1:
        metadata = {}
        metadata["ms_timestamp"] = data.read("Q")
        metadata["samplerate"] = data.read("I")
        metadata["no_of_samples"] = data.read("I")
        metadata["maxvoltage"] = data.read("d")
        metadata["maxdeviation"] = data.read("d")
        metadata["affected_channels"] = data.read("H")

        if only_metadata:
            return metadata

        data_lengths = data.read("8I")
        versions = data.read("8H")
        data_list = []
        for length, version in zip(data_lengths, versions):
            data_buffer = zlib.decompress(
                packed_data[data.pointer : data.pointer + length]
            )
            if version == 1:
                data_list.append(np.frombuffer(data_buffer, dtype=np.float32))
            elif version == 2:
                data0 = np.array(struct.unpack("f", data_buffer[:4]))
                data_rest = data0 + np.cumsum(
                    np.frombuffer(data_buffer, dtype=np.float32, offset=4)
                )
                data_list.append(np.concatenate((data0, data_rest)))
            elif version == 3 or version == 4:
                u_recr = unpack3(data_buffer)
                data_list.append(u_recr)
            data.pointer += length

    elif pak_version == 3:
        metadata = {}
        metadata["ms_timestamp"] = data.read("Q")
        metadata["samplerate"] = data.read("I")
        metadata["no_of_channels"] = data.read("H")
        no_of_bytes_in_channel_name_pack = data.read("H")
        if no_of_bytes_in_channel_name_pack == 0:
            metadata["channel_names"] = [
                f"CH{i}" for i in range(metadata["no_of_channels"], 1)
            ]
        else:
            metadata["channel_names"] = (
                data.read_raw(no_of_bytes_in_channel_name_pack)
                .decode("utf-8")
                .split("\t")
            )
        metadata["no_of_samples"] = data.read("I")
        metadata["maxvoltage"] = data.read("d")
        metadata["maxdeviation"] = data.read("d")
        metadata["affected_channels"] = data.read("H")

        if only_metadata:
            return metadata

        decompressed_rest = zlib.decompress(data.read_rest_raw())
        data_buffer = bindata(decompressed_rest)
        data_list = []
        for i in range(metadata["no_of_channels"]):
            data0 = np.array(data_buffer.read("f"))
            data_rest = data0 + np.cumsum(
                np.array(data_buffer.read(f'{metadata["no_of_samples"]-1}f'))
            )
            data_list.append(np.concatenate((data0, data_rest), axis=None))

    else:
        print(f"pak_version {pak_version} unknown")

    return data_list, metadata


def unpack_metadata(packed_data):
    data = bindata(packed_data)
    pak_version = data.read("H")
    if not pak_version == 1:
        print(f"pak_version {pak_version} unknown")
    metadata = {}
    metadata["ms_timestamp"] = data.read("Q")
    metadata["samplerate"] = data.read("I")
    metadata["no_of_samples"] = data.read("I")
    metadata["maxvoltage"] = data.read("d")
    metadata["maxdeviation"] = data.read("d")
    metadata["affected_channels"] = data.read("H")
    return metadata


def unpack3(pack):
    version, ms_timestamp, samplerate, length = struct.unpack("=HdII", pack[:18])
    freqs = struct.unpack("=30f", pack[18:138])
    amps = struct.unpack("=30f", pack[138:258])
    phases = struct.unpack("=30f", pack[258:378])

    u_recr = recreate_from_components(freqs, amps, phases, samplerate, length)
    u_recr += np.frombuffer(zlib.decompress(pack[378:]), dtype=np.float32)

    return u_recr


def cos_components(data, num_components=30):
    fft_data = mkl_fft.fft(data)
    amps = np.abs(fft_data[: int(fft_data.size / 2 + 1)] * (2 / data.size))
    X = fft_data[: int(fft_data.size / 2 + 1)]
    X[np.abs(X) < 0.001] = 0  # Necessary for correct phase
    phases = np.angle(X)
    freqs = np.linspace(0, SAMPLE_RATE / 2, num=amps.size)

    max_amp_indices = np.argsort(amps)[-num_components:]
    relevant_amps = amps[max_amp_indices]
    relevant_phases = phases[max_amp_indices]
    relevant_freqs = freqs[max_amp_indices]
    return relevant_freqs, relevant_amps, relevant_phases


def recreate_from_components(freqs, amps, phases, sample_rate, length):
    u_recr = np.zeros(length)
    t = np.arange(length)
    for freq, amp, phase in zip(freqs, amps, phases):
        u_recr += amp * np.cos(freq * 2 * np.pi * t / sample_rate + phase)
    return u_recr


if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import glob
    import random

    allfiles = glob.glob("../testtransients/**/*.json")
    # print(allfiles)
    random.shuffle(allfiles)
    for jsonfile in allfiles:
        # if 'nellingen' not in jsonfile:
        #     continue
        data_list = []
        size = os.stat(jsonfile).st_size
        print(f"{jsonfile}: {size//1000} kB", end=" --> ")
        with open(jsonfile, "r") as f:
            d = json.load(f)
        if "CH8" not in d.keys():
            print(" nope")
            continue
        for key, value in d.items():
            if type(value) == type([]):
                data_list.append(np.array(value, dtype=np.float16))

        starttime = time.time()
        pak = pack(data_list, time.time(), 1e6)
        runtime = time.time() - starttime
        print(f"PAK: ({round(runtime * 1000)} ms), {len(pak)//1000} kB")
        time.sleep(0.001)

        starttime = time.time()
        pak_simple = pack_simple(data_list, time.time(), 1e6)
        runtime = time.time() - starttime
        print(f"PAK: ({round(runtime * 1000)} ms), {len(pak_simple)//1000} kB")
        time.sleep(0.001)

        # starttime = time.time()
        # pak2 = pack2(data_list, time.time(), 1e6)
        # print(f'({round((time.time() - starttime) * 1000)} ms)', end=' - ')
        # print(f'{len(pak2)//1000} kB')

        ms_timestamp, samplerate, data_list_unpacked = unpack(pak)

        # for d in data_list_unpacked:
        #     print(d.size)

        for org, unp in zip(data_list, data_list_unpacked):
            plt.plot(org)
            plt.plot(unp)
            plt.grid(True)
            plt.show()

            # wave = np.array(value)
            # starttime = time.time()
            # packed_data = pack(wave, SAMPLE_RATE)
            # print(time.time() - starttime)
            # compressed_size = len(packed_data)
            # compressed_wave = unpack(packed_data)

            # res_abs = np.abs(wave-compressed_wave)
            # print(f'{key}: {size//8} -> {compressed_size} ({compressed_size/(size//8)*100:.1f}%)')
            # print(f'Mean Residual: {np.mean(res_abs):.3f} V, Max. Residual: {np.max(res_abs):.3f} V')

            # plt.plot(wave, color='r')
            # plt.plot(compressed_wave, color='b')
            # plt.plot(res_abs, color='g')
            # plt.title(f'{jsonfile} - {key}')
            # plt.grid()
            # plt.show()


# plt.plot(u1)
# plt.plot(u_recr+res)
# plt.grid()
# plt.show()

# print(len(res_unzip))
# plt.plot(res_unzip)
# plt.show()
