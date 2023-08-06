import pytest
import datetime
import numpy as np
from transpak import pack, unpack


@pytest.fixture
def create_simple_transient():
    data_list = []
    for ch in range(8):
        signal = np.random.random(20000).astype(np.float32)
        data_list.append(signal)
    ms_timestamp = int(datetime.datetime.now().timestamp() * 1000)
    samplerate = 1000000
    channel_names = list("ABCDEFGH")
    peak = 420
    max_deviation = 69
    affected_channels = [0]

    return (
        data_list,
        ms_timestamp,
        samplerate,
        peak,
        max_deviation,
        affected_channels,
        channel_names,
    )


@pytest.fixture
def create_big_transient():
    data_list = []
    for ch in range(8):
        signal = np.random.random(20000).astype(np.float32)
        data_list.append(signal)
    ms_timestamp = int(datetime.datetime.now().timestamp() * 1000)
    samplerate = 1000000
    channel_names = [
        "Channel 1",
        "#$!@#!)",
        " ",
        "!@#$%^&*()_+|",
        "CHANNEL5",
        "",
        "1",
        "1",
        "Channel 9",
        "b",
        ".",
        "Channel 12",
    ]
    peak = 1000
    max_deviation = 0
    affected_channels = [0, 1, 11]

    return (
        data_list,
        ms_timestamp,
        samplerate,
        peak,
        max_deviation,
        affected_channels,
        channel_names,
    )


def test_v1_simple(create_simple_transient):

    transient_data = create_simple_transient

    (
        data_list,
        ms_timestamp,
        samplerate,
        peak,
        max_deviation,
        affected_channels,
        channel_names,
    ) = transient_data

    pak = pack(*transient_data, pak_version=1)
    metadata = unpack(pak, only_metadata=True)
    assert metadata["ms_timestamp"] == ms_timestamp
    assert metadata["samplerate"] == samplerate
    assert metadata["maxvoltage"] == peak
    assert metadata["maxdeviation"] == max_deviation

    data, metadata = unpack(pak)
    for i, signal in enumerate(data_list):
        assert np.allclose(signal, data[i])


def test_v4_simple(create_simple_transient):

    transient_data = create_simple_transient

    (
        data_list,
        ms_timestamp,
        samplerate,
        peak,
        max_deviation,
        affected_channels,
        channel_names,
    ) = transient_data

    pak = pack(*transient_data, pak_version=4)
    metadata = unpack(pak, only_metadata=True)
    assert metadata["ms_timestamp"] == ms_timestamp
    assert metadata["samplerate"] == samplerate
    assert metadata["peak"] == peak
    assert metadata["max_deviation"] == max_deviation

    data, metadata = unpack(pak)
    for i, signal in enumerate(data_list):
        assert np.size(signal) == np.size(data[i])
        assert np.allclose(signal, data[i], atol=1e-5)
