"""
These tests are aimed to ensure that the `RawIOChunk` instances behave consistently with
the other `RawIOBase` implementations.
"""

import os
import re
from io import SEEK_CUR, SEEK_END, BytesIO, RawIOBase
from itertools import product
from tempfile import TemporaryFile
from typing import IO, Callable, Type

import pytest

from io_chunks.chunks import RawIOChunk

RawIOFactory = Callable[[], RawIOBase]


def temp_file_factory(contents: bytes, buffering=-1) -> IO:
    temp_file = TemporaryFile("w+b", buffering=buffering)
    temp_file.write(contents)
    temp_file.seek(0)
    return temp_file


@pytest.mark.parametrize(
    ["factory", "readed"],
    [
        (lambda: BytesIO(b"01234"), b"01234"),
        (lambda: RawIOChunk(BytesIO(b"01234"), size=4), b"0123"),
        (lambda: RawIOChunk(BytesIO(b"01234"), size=5), b"01234"),
        (lambda: RawIOChunk(BytesIO(b"01234"), size=6), b"01234"),
        (lambda: temp_file_factory(b"01234"), b"01234"),
        (lambda: temp_file_factory(b"01234", buffering=0), b"01234"),
    ],
)
def test_read(factory: RawIOFactory, readed: bytes):
    with factory() as instance:
        result = instance.read()
        assert result == readed
        assert instance.read() == b""
        assert instance.read(1) == b""


@pytest.mark.parametrize(
    ["factory", "action"],
    product(
        [
            lambda: BytesIO(b"000"),
            lambda: RawIOChunk(BytesIO(b"000"), size=1),
            lambda: temp_file_factory(b"000"),
            lambda: temp_file_factory(b"000", buffering=0),
        ],
        [
            lambda buffer: buffer.read(),
            lambda buffer: buffer.seek(0),
            lambda buffer: buffer.tell(),
            lambda buffer: buffer.seekable(),
            lambda buffer: buffer.readable(),
        ],
    ),
)
def test_closed_raise_value_error(
    factory: RawIOFactory, action: Callable[[RawIOBase], None]
):
    with factory() as instance:
        assert instance.closed is False
        instance.close()
        assert instance.closed is True


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=1),
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
)
def test_closed_values(factory: RawIOFactory):
    with factory() as instance:
        assert instance.tell() == 0
        assert instance.seek(0) == 0
        assert instance.readable() is True
        assert instance.seekable() is True


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=1),
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
    ids=["BytesIO", "RawIOChunk", "TempFile", "TempFile (unbuffered)"],
)
def test_extra_seek(factory: RawIOFactory):
    with factory() as instance:
        assert instance.seek(100) == 100
        assert instance.tell() == 100


@pytest.mark.parametrize(
    ["factory", "exception"],
    [
        (lambda: BytesIO(b"000"), ValueError),
        (lambda: RawIOChunk(BytesIO(b"000"), size=1), ValueError),
        (lambda: temp_file_factory(b"000"), OSError),
        (lambda: temp_file_factory(b"000", buffering=0), OSError),
    ],
    ids=["BytesIO", "RawIOChunk", "TempFile", "TempFile (unbuffered)"],
)
def test_negative_seek(factory: RawIOFactory, exception: Type[Exception]):
    with factory() as instance:
        with pytest.raises(exception):
            assert instance.seek(-10) == -10


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=3),
    ],
    ids=["BytesIO", "RawIOChunk"],
)
def test_relative_seek(factory: RawIOFactory):
    with factory() as instance:
        assert instance.seek(0) == 0
        assert instance.seek(-2, SEEK_END) == 1
        assert instance.seek(1, SEEK_CUR) == 2
        assert instance.seek(-1, SEEK_CUR) == 1
        assert instance.seek(-1, SEEK_CUR) == 0
        assert instance.seek(-1, SEEK_CUR) == 0
        assert instance.seek(-4, SEEK_END) == 0


@pytest.mark.parametrize(
    "factory",
    [
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
    ids=["TempFile", "TempFile (unbuffered)"],
)
def test_relative_seek_oserror(factory: RawIOFactory):
    with factory() as instance:
        assert instance.seek(0) == 0
        assert instance.seek(-2, SEEK_END) == 1
        assert instance.seek(1, SEEK_CUR) == 2
        assert instance.seek(-1, SEEK_CUR) == 1
        assert instance.seek(-1, SEEK_CUR) == 0
        with pytest.raises(OSError, match=re.escape(r"[Errno 22] Invalid argument")):
            instance.seek(-1, SEEK_CUR)
        with pytest.raises(OSError, match=re.escape(r"[Errno 22] Invalid argument")):
            assert instance.seek(-4, SEEK_END) == 0


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=1),
    ],
)
def test_seek_hole_error(factory: RawIOFactory):
    with factory() as instance:
        with pytest.raises(ValueError):
            instance.seek(0, os.SEEK_DATA)
        with pytest.raises(ValueError):
            instance.seek(0, os.SEEK_HOLE)


@pytest.mark.parametrize(
    "factory",
    [
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
)
def test_seek_hole_valid(factory: RawIOFactory):
    with factory() as instance:
        assert instance.seek(0, os.SEEK_DATA) == 0
        assert instance.seek(0, os.SEEK_HOLE) == 3


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=1),
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
)
def test_pos_invalid_type(factory: RawIOFactory):
    with factory() as instance:
        with pytest.raises(TypeError):
            instance.seek("a")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            instance.seek(1, "a")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=1),
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
)
def test_readinto_empty_array(factory: RawIOFactory):
    with factory() as instance:
        buffer = bytearray(0)
        assert instance.readinto(buffer) == 0
        assert buffer == b""


@pytest.mark.parametrize(
    ["factory", "readed"],
    [
        (lambda: BytesIO(b"000"), b"00"),
        (lambda: RawIOChunk(BytesIO(b"000"), size=3), b"00"),
        (lambda: temp_file_factory(b"000"), b"00"),
        (lambda: temp_file_factory(b"000", buffering=0), b"00"),
    ],
    ids=["BytesIO", "RawIOChunk", "TempFile", "TempFile (unbuffered)"],
)
def test_truncate(factory: RawIOFactory, readed: bytes):
    with factory() as instance:
        assert instance.truncate(2) == 2
        assert instance.read() == readed


@pytest.mark.parametrize(
    ["factory", "exception"],
    [
        (lambda: BytesIO(b"000"), ValueError),
        (lambda: RawIOChunk(BytesIO(b"000"), size=1), ValueError),
        (lambda: temp_file_factory(b"000"), OSError),
        (lambda: temp_file_factory(b"000", buffering=0), OSError),
    ],
    ids=["BytesIO", "RawIOChunk", "TempFile", "TempFile (unbuffered)"],
)
def test_truncate_negative(factory: RawIOFactory, exception: Type[Exception]):
    with factory() as instance:
        with pytest.raises(exception):
            assert instance.truncate(-1) == 0
