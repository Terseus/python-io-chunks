from __future__ import annotations

from io import (
    SEEK_CUR,
    SEEK_END,
    SEEK_SET,
    BufferedIOBase,
    RawIOBase,
    UnsupportedOperation,
)
from types import TracebackType
from typing import IO, Optional, Type, Union

from .exceptions import ClosedStreamError


class RawIOChunk(RawIOBase, IO):
    """
    An IO read-only object with access to a portion of another IO object.
    In other terms, a sub-stream of a stream.

    It's meant to be used with file-like objects from `open` so you can divide
    the file stream in chunks without having an in-memory copy of all of its
    contents.
    """

    def __init__(
        self,
        stream: Union[RawIOBase, BufferedIOBase],
        size: int,
        start: Optional[int] = None,
    ) -> None:
        """
        Creates a new RawIOChunk.

        :param stream: An IO of file-like object with the original stream;
            must be seekable.
        :type stream: RawIOBase or BufferedIOBase
        :param int size: The size of the chunk.
        :param start: The start position in the original stream; if `None` it
            uses the current stream position.
        :type start: int or None
        :raises ValueError: If `stream` is closed or not seekable.
        """
        super().__init__()
        if not isinstance(stream, (RawIOBase, BufferedIOBase)):
            raise TypeError(
                f"stream: expected RawIOBase or BufferedIOBase, got {type(stream)}"
            )
        if not stream.seekable():
            raise ValueError("stream: buffer is not seekable")
        if stream.closed:
            raise ValueError("stream: buffer is closed")
        if not isinstance(size, int):
            raise TypeError(f"size: expected int, got {type(size)}")
        if start is None:
            start = stream.tell()
        elif not isinstance(start, int):
            raise TypeError(f"start: expected int, got {type(start)}")
        self._start = start
        self._size = size
        self._cursor = 0
        self._stream = stream
        self._closed = False

    @property
    def size(self) -> int:
        """Size of the chunk."""
        return self._size

    @property
    def start(self) -> int:
        """Start position of the chunk."""
        return self._start

    @property
    def end(self) -> int:
        """End position of the chunk"""
        return self._start + self._size

    def __enter__(self) -> RawIOChunk:
        if self.closed:
            raise ClosedStreamError()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    # The type definition of `array` in `RawIOBase` of Python 3.7 is as
    # follows:
    #     `Union[bytearray, memoryview, array[Any], mmap, _CData]`
    # Given that _CData is a private class of the types module we cannot
    # fulfill the type definition here, that's why we ignore it.
    def readinto(  # type: ignore[override]
        self, array: Union[bytearray, memoryview]
    ) -> Union[int, None]:
        """
        Read bytes into a pre-allocated array using at most one call to the underlying
        stream.

        If the underlying stream is closed raises `ValueError`.
        If there si no more bytes to read in the underlying stream writes nothing and
        return 0, even if there was remaining bytes in the chunk.
        """
        if self.closed:
            raise ClosedStreamError()
        if len(array) == 0:
            return 0
        remaining = self._size - self._cursor
        if remaining <= 0:
            return 0
        array = memoryview(array)
        array = array.cast("B")
        position = self._stream.tell()
        self._stream.seek(self._start + self._cursor)
        if len(array) > remaining:
            array = array[:remaining]
        read_size = self._stream.readinto(array)
        if read_size is None:
            return None
        if read_size == 0:
            return 0
        self._cursor += read_size
        self._stream.seek(position)
        return read_size

    def seek(self, pos: int, whence: int = 0) -> int:
        if self.closed:
            raise ClosedStreamError()
        if not isinstance(pos, int):
            raise TypeError(f"pos: expected int, got {type(pos)}")
        if not isinstance(whence, int):
            raise TypeError(f"whence: expected int, got {type(whence)}")
        if whence == SEEK_SET:
            if pos < 0:
                raise ValueError(f"negative seek value {pos}")
            self._cursor = pos
        elif whence == SEEK_CUR:
            self._cursor += pos
        elif whence == SEEK_END:
            self._cursor = self._size + pos
        else:
            raise ValueError(f"whence: invalid value: {whence}")
        if self._cursor < 0:
            self._cursor = 0
        return self._cursor

    def truncate(self, size: Optional[int] = None) -> int:
        """
        Resize the chunk to the given size, or to the current position if size is
        `None`.
        The current position isn't changed.
        """
        if size is None:
            size = self._cursor
        elif size < 0:
            raise ValueError(f"negative size value {size}")
        self._size = size
        return self._size

    def tell(self) -> int:
        if self.closed:
            raise ClosedStreamError()
        return self._cursor

    def seekable(self) -> bool:
        if self.closed:
            raise ClosedStreamError()
        return True

    def readable(self) -> bool:
        if self.closed:
            raise ClosedStreamError()
        return True

    def close(self) -> None:
        """
        Mark this instance as closed.

        Does NOT close the underlying stream.
        """
        self._closed = True

    @property
    def closed(self) -> bool:
        """
        Returns whenever the underlying stream or this instance are closed.
        """
        return self._stream.closed or self._closed

    def write(self, bytes) -> int:
        """
        This streams doesn't support writing.

        :raises UnsupportedOperation:
        """
        raise UnsupportedOperation("This stream doesn't support write")

    def fileno(self) -> int:
        """
        Returns the underlying stream `fileno`.
        """
        return self._stream.fileno()
