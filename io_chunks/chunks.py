# -*- coding: utf-8 -*-


from io import (
    RawIOBase, IOBase, SEEK_SET, SEEK_CUR, SEEK_END, UnsupportedOperation
)
from six import integer_types


class RawIOChunk(RawIOBase):
    """
    An IO read-only object with access to a portion of another IO object.
    In other terms, a sub-stream of a stream.

    It's meant to be used with file-like objects from `open` so you can divide
    the file stream in chunks without having an in-memory copy of all of its
    contents.
    """

    size = property(lambda s: s._size)
    start = property(lambda s: s._start)
    end = property(lambda s: s._start + s._size)

    def __init__(self, stream, size, start=None):
        """
        Creates a new RawIOChunk.

        Args:
            stream: An IO or file-like object with the original stream; must
                be seekable.
            size: The size of the chunk.
            start: The start position in the original stream; if `None` it
                uses the current stream position.
        """
        if not isinstance(stream, IOBase):
            raise TypeError("stream: expected IOBase, got {0!s}"
                            .format(stream))
        if not stream.seekable():
            raise ValueError("Buffer is not seekable")
        if stream.closed:
            raise ValueError("Buffer is closed")
        if not isinstance(size, integer_types):
            raise TypeError("size: expected int, got {0!s}"
                            .format(type(size)))
        if start is None:
            start = stream.tell()
        elif not isinstance(start, integer_types):
            raise TypeError("start: expected int, got {0!s}"
                            .format(type(start)))
        self._start = start
        self._size = size
        self._cursor = 0
        self._stream = stream
        super(RawIOChunk, self).__init__()

    def readinto(self, array):
        if not isinstance(array, (bytearray, memoryview)):
            raise TypeError(
                "array: expected bytearray or memoryview, got {0!s}"
                .format(type(array))
            )
        if self.closed:
            raise ValueError("I/O operation on closed stream")
        if len(array) == 0:
            return 0
        remaining = self._size - self._cursor
        if remaining <= 0:
            return 0
        array = memoryview(array)
        try:
            array = array.cast('B')
        except AttributeError:
            pass  # Python <=3.2 doesn't support format casting :(
        position = self._stream.tell()
        self._stream.seek(self._start + self._cursor)
        if len(array) > remaining:
            array = array[:remaining]
        read_size = self._stream.readinto(array)
        if read_size is None:
            return None
        if read_size == 0:
            raise EOFError("End of file while reading original stream")
        self._cursor += read_size
        self._stream.seek(position)
        return read_size

    def seek(self, pos, whence=0):
        if not isinstance(pos, integer_types):
            raise TypeError("pos: expected int, got {0!s}".format(type(pos)))
        if not isinstance(whence, integer_types):
            raise TypeError("whence: expected int, got {0!s}"
                            .format(type(whence)))
        if whence == SEEK_SET:
            self._cursor = pos
        elif whence == SEEK_CUR:
            self._cursor += pos
        elif whence == SEEK_END:
            self._cursor = self._size + pos
        else:
            raise ValueError("whence: invalid value: {0!s}".format(whence))
        return self._cursor

    def tell(self):
        return self._cursor

    def seekable(self):
        return True

    def readable(self):
        return True

    def close(self):
        raise UnsupportedOperation(
            "This stream cannot be closed, close the underlying stream instead"
        )

    @property
    def closed(self):
        return self._stream.closed

    def write(self, *args, **kwargs):
        raise UnsupportedOperation("This stream doesn't support write")

    def fileno(self):
        return self._stream.fileno()
