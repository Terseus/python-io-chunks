# -*- coding: utf-8 -*-
"""TODO: doc module"""


import unittest
from io import BytesIO, SEEK_CUR, SEEK_END
from io_chunks import RawIOChunk
from nose.tools import assert_raises, eq_, ok_


class TestRawIOChunk(unittest.TestCase):
    """TODO: doc class"""

    STRINGS = [
        b'hello',
        b'beautiful',
        b'world',
    ]

    def get_raw_buffer(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        return BytesIO(b''.join(self.STRINGS))

    def test_file_begin(self):
        """Testcase named: test_file_begin"""
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[0]))
            eq_(chunk.start, 0)
            eq_(chunk.size, len(self.STRINGS[0]))
            eq_(chunk.end, chunk.start + chunk.size)
            eq_(chunk.tell(), chunk.start)
            eq_(chunk.read(), self.STRINGS[0])
            eq_(chunk.tell(), chunk.end)

    def test_file_middle(self):
        """Testcase named: test_file_middle"""
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[1]),
                               len(self.STRINGS[0]))
            eq_(chunk.read(), self.STRINGS[1])

    def test_eof(self):
        """Testcase named: test_eof"""
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
        """Testcase named: test_closed"""
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[0]))
            ok_(not chunk.closed)
        ok_(chunk.closed)
        with assert_raises(ValueError):
            chunk.read()

    def test_seek(self):
        """Testcase named: test_seek"""
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
        """Testcase named: test_full_file"""
        with self.get_raw_buffer() as data_file:
            chunks = [RawIOChunk(data_file, len(self.STRINGS[0]))]
            chunks.append(RawIOChunk(data_file, len(self.STRINGS[1]),
                                     chunks[0].end))
            chunks.append(RawIOChunk(data_file, len(self.STRINGS[2]),
                                     chunks[1].end))
            eq_(sum(chunk.size for chunk in chunks),
                len(b''.join(self.STRINGS)))
