# -*- coding: utf-8 -*-


import unittest
from io_extra import RawIOChunk
from io import SEEK_END, SEEK_CUR, BytesIO
from nose.tools import eq_, ok_, assert_raises


class TestRawIOChunk(unittest.TestCase):
    STRINGS = [
        b'hello',
        b'beautiful',
        b'world',
    ]

    def get_raw_buffer(self):
        return BytesIO(b''.join(self.STRINGS))

    def test_file_begin(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[0]))
            eq_(chunk.start, 0)
            eq_(chunk.size, len(self.STRINGS[0]))
            eq_(chunk.end, chunk.start + chunk.size)
            eq_(chunk.tell(), chunk.start)
            eq_(chunk.read(), self.STRINGS[0])
            eq_(chunk.tell(), chunk.end)

    def test_file_middle(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[1]),
                               len(self.STRINGS[0]))
            eq_(chunk.read(), self.STRINGS[1])

    def test_eof(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[2]) + 1,
                               len(self.STRINGS[0]) + len(self.STRINGS[1]))
            with assert_raises(EOFError):
                chunk.read()
            chunk.seek(0)
            eq_(chunk.read(chunk.size - 1), self.STRINGS[2])
            with assert_raises(EOFError):
                chunk.read(1)

    def test_closed(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[0]))
            ok_(not chunk.closed)
        ok_(chunk.closed)
        with assert_raises(ValueError):
            chunk.read()

    def test_seek(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[1]),
                               len(self.STRINGS[0]))
            eq_(chunk.seek(1), 1)
            eq_(chunk.tell(), 1)
            eq_(chunk.seek(1, SEEK_CUR), 2)
            eq_(chunk.tell(), 2)
            eq_(chunk.seek(-1, SEEK_END), len(self.STRINGS[1]) - 1)
            eq_(chunk.tell(), len(self.STRINGS[1]) - 1)
            eq_(chunk.seek(0), 0)
            eq_(chunk.read(), self.STRINGS[1])
            eq_(chunk.seek(0), 0)
            eq_(chunk.read(), self.STRINGS[1])

    def test_full_file(self):
        with self.get_raw_buffer() as data_file:
            chunks = [RawIOChunk(data_file, len(self.STRINGS[0]))]
            chunks.append(RawIOChunk(data_file, len(self.STRINGS[1]),
                                     chunks[0].end))
            chunks.append(RawIOChunk(data_file, len(self.STRINGS[2]),
                                     chunks[1].end))
            eq_(sum(chunk.size for chunk in chunks),
                len(b''.join(self.STRINGS)))
