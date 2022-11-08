from io import SEEK_CUR, SEEK_END, BytesIO

import pytest

from io_chunks.chunks import ClosedStreamError, RawIOChunk


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
    with pytest.raises(ClosedStreamError):
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


@pytest.mark.parametrize(
    "action",
    [
        lambda buffer: buffer.read(),
        lambda buffer: buffer.seek(0),
        lambda buffer: buffer.tell(),
        lambda buffer: buffer.seekable(),
        lambda buffer: buffer.readable(),
    ],
)
def test_closed_stream_error(action):
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        chunk.close()
        with pytest.raises(ClosedStreamError):
            action(chunk)


def test_context_manager():
    with BytesIO(b"0123456789") as buffer:
        with RawIOChunk(buffer, size=5) as chunk:
            assert chunk.closed is False
        assert chunk.closed is True


def test_double_context_manager_fails():
    with BytesIO(b"0123456789") as buffer:
        chunk = RawIOChunk(buffer, size=5)
        with chunk as _:
            pass
        with pytest.raises(ClosedStreamError):
            with chunk as _:
                pass
