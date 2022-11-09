"""
These tests are aimed to ensure that the `RawIOChunk` instances behave consistently with
the other `IOBase` implementations.
"""

from io import BytesIO, IOBase, StringIO
from itertools import product
from tempfile import TemporaryFile
from typing import IO, Callable, Type, Union

import pytest

from io_chunks.chunks import RawIOChunk

IOFactory = Callable[[], Union[IO, IOBase]]


def temp_file_factory(contents: bytes, buffering=-1) -> IO:
    temp_file = TemporaryFile("w+b", buffering=buffering)
    temp_file.write(contents)
    temp_file.seek(0)
    return temp_file


@pytest.mark.parametrize(
    ["factory", "readed", "empty"],
    [
        (lambda: BytesIO(b"01234"), b"01234", b""),
        (lambda: StringIO("01234"), "01234", ""),
        (lambda: RawIOChunk(BytesIO(b"01234"), size=4), b"0123", b""),
        (lambda: RawIOChunk(BytesIO(b"01234"), size=5), b"01234", b""),
        (lambda: RawIOChunk(BytesIO(b"01234"), size=6), b"01234", b""),
        (lambda: temp_file_factory(b"01234"), b"01234", b""),
        (lambda: temp_file_factory(b"01234", buffering=0), b"01234", b""),
    ],
)
def test_read(factory: IOFactory, readed: Union[bytes, str], empty: Union[bytes, str]):
    with factory() as instance:
        result = instance.read()
        assert result == readed
        assert instance.read() == empty
        assert instance.read(1) == empty


@pytest.mark.parametrize(
    ["factory", "action"],
    product(
        [
            lambda: BytesIO(b"000"),
            lambda: StringIO("000"),
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
def test_closed_raise_value_error(factory: IOFactory, action: Callable[[IO], None]):
    with factory() as instance:
        assert instance.closed is False
        instance.close()
        assert instance.closed is True


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: StringIO("000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=1),
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
)
def test_closed_values(factory: IOFactory):
    with factory() as instance:
        assert instance.tell() == 0
        assert instance.seek(0) == 0
        assert instance.readable() is True
        assert instance.seekable() is True


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BytesIO(b"000"),
        lambda: StringIO("000"),
        lambda: RawIOChunk(BytesIO(b"000"), size=1),
        lambda: temp_file_factory(b"000"),
        lambda: temp_file_factory(b"000", buffering=0),
    ],
    ids=["BytesIO", "StringIO", "RawIOChunk", "TempFile", "TempFile (unbuffered)"],
)
def test_extra_seek(factory: IOFactory):
    with factory() as instance:
        assert instance.seek(100) == 100
        assert instance.tell() == 100


@pytest.mark.parametrize(
    ["factory", "exception"],
    [
        (lambda: BytesIO(b"000"), ValueError),
        (lambda: StringIO("000"), ValueError),
        (lambda: RawIOChunk(BytesIO(b"000"), size=1), ValueError),
        (lambda: temp_file_factory(b"000"), OSError),
        (lambda: temp_file_factory(b"000", buffering=0), OSError),
    ],
    ids=["BytesIO", "StringIO", "RawIOChunk", "TempFile", "TempFile (unbuffered)"],
)
def test_negative_seek(factory: IOFactory, exception: Type[Exception]):
    with factory() as instance:
        with pytest.raises(exception):
            assert instance.seek(-10) == -10
