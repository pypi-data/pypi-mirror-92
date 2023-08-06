import os
import time
import json
import struct
import zlib

import numpy as np


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


# Pack Functions:
# ===============


def pack_data(data_list, samplerate):
    versions = []
    data_lengths = []
    data_paks = []
    for data in data_list:
        paksizes = []
        paks_temp = []
        # for ver in (1, 2, 3, 4):
        for ver in (1, 2):
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
    # elif version == 3 or version == 4:
    #     num_components = 30
    #     freqs, amps, phases = cos_components(data, num_components=num_components)
    #     pack = struct.pack(f"{num_components}f", *freqs)
    #     pack += struct.pack(f"{num_components}f", *amps)
    #     pack += struct.pack(f"{num_components}f", *phases)
    #     u_recr = recreate_from_components(freqs, amps, phases, samplerate, data.size)
    #     res = data - u_recr
    #     if version == 3:
    #         pack += struct.pack(f"{len(data)}f", *res)
    #     if version == 4:
    #         pack += struct.pack(f"{len(data)}f", res[0], *np.diff(res))
    return pack


def calc_affected_channels_code(affected_channels, max_channels=8):
    affected_channels_code = 0
    for i in range(max_channels):
        if i in affected_channels:
            affected_channels_code += 2 ** i
    return affected_channels_code


# Pack Functions:
# ===============


def pack(
    data_list,
    ms_timestamp,
    samplerate,
    peak=0,
    maxdeviation=0,
    affected_channels=[],
    channel_names=[],
    pak_version=4,
):

    if pak_version == 1:
        pack = struct.pack("H", int(pak_version))
        pack += struct.pack("Q", int(ms_timestamp))
        pack += struct.pack("I", int(samplerate))
        pack += struct.pack("I", data_list[0].size)
        pack += struct.pack("d", peak)
        pack += struct.pack("d", maxdeviation)
        pack += struct.pack("H", calc_affected_channels_code(affected_channels))

        versions, data_lengths, data_paks = pack_data(data_list, samplerate)
        pack += struct.pack("8I", *data_lengths)
        pack += struct.pack("8H", *versions)

        for data_pak in data_paks:
            pack += data_pak

        return pack

    ## Version 4
    # - prepared for 16 channels (number is variable)
    # - diff-packing only
    # - zlib-compression of all channels together
    # - Encode channel names with '\t' as separator
    elif pak_version == 4:

        affected_channels_code = calc_affected_channels_code(
            affected_channels, max_channels=16
        )

        if not channel_names:
            print(f"No channel names given")
            channel_names = [""] * len(data_list)
        if len(channel_names) is not len(data_list):
            print(
                f"Different number of channels in channel_names ({len(channel_names)}) and data_list ({len(data_list)})"
            )

        pack = struct.pack("H", int(pak_version))
        pack += struct.pack("Q", int(ms_timestamp))
        pack += struct.pack("I", int(samplerate))
        pack += struct.pack("H", len(data_list))  # Number of channels
        channels_names_pack = b"\t".join(
            [ch_name.encode("utf-8") for ch_name in channel_names]
        )
        pack += struct.pack(
            "H", len(channels_names_pack)
        )  # Number of bytes in channel_names_pack
        pack += channels_names_pack
        pack += struct.pack("I", data_list[0].size)  # Number of samples per channel
        pack += struct.pack("d", peak)
        pack += struct.pack("d", maxdeviation)
        pack += struct.pack("H", int(affected_channels_code))

        # Pack data as diff and compress:
        datapack = b"".join(
            struct.pack(f"{len(data)}f", data[0], *np.diff(data)) for data in data_list
        )
        datapack = zlib.compress(datapack)

        pack += datapack

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

    ## Version 4:
    elif pak_version == 4:
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
        metadata["peak"] = data.read("d")
        metadata["max_deviation"] = data.read("d")
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
