from io import SEEK_CUR, SEEK_END, BytesIO

import pytest

from io_chunks import RawIOChunk


def test_file_begin():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        assert chunk.start == 0
        assert chunk.size == 5
        assert chunk.end == 5
        assert chunk.tell() == 0
        assert chunk.read() == b"01234"
        assert chunk.tell() == 5


def test_file_middle():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5, start=2)
        assert chunk.read() == b"23456"


def test_read_until_eof():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=6, start=5)
        assert chunk.read() == b"56789"


def test_read_past_eof():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=1, start=9)
        assert chunk.read(1) == b"9"
        assert chunk.read(1) == b""


def test_eof():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, 6, 5)
        assert chunk.read() == b"56789"
        chunk.seek(0)
        assert chunk.read(5) == b"56789"
        assert chunk.read() == b""


def test_stream_closed():
    with BytesIO(b"01234") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        assert chunk.closed is False
    assert chunk.closed is True
    with pytest.raises(ValueError):
        chunk.read()


def test_seek():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5, start=5)
        assert chunk.tell() == 0
        assert chunk.seek(1) == 1
        assert chunk.tell() == 1
        assert chunk.seek(1, SEEK_CUR) == 2
        assert chunk.tell() == 2
        assert chunk.seek(-1, SEEK_END) == 4
        assert chunk.seek(2) == 2
        assert chunk.read() == b"789"
        assert chunk.seek(0) == 0
        assert chunk.read() == b"56789"


def test_close():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        chunk.close()
        assert chunk.closed is True
        assert buffer.closed is False


def test_closed_read_error():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        chunk.close()
        with pytest.raises(ValueError):
            chunk.read()


def test_closed_seek_error():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        chunk.close()
        with pytest.raises(ValueError):
            chunk.seek(0)


def test_closed_tell_error():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        chunk.close()
        with pytest.raises(ValueError):
            chunk.tell()
