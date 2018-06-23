# -*- coding: utf-8 -*-


import unittest
from io_chunks import RawIOChunk
from io import SEEK_END, SEEK_CUR, BytesIO


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
            self.assertEqual(chunk.start, 0)
            self.assertEqual(chunk.size, len(self.STRINGS[0]))
            self.assertEqual(chunk.end, chunk.start + chunk.size)
            self.assertEqual(chunk.tell(), chunk.start)
            self.assertEqual(chunk.read(), self.STRINGS[0])
            self.assertEqual(chunk.tell(), chunk.end)

    def test_file_middle(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[1]),
                               len(self.STRINGS[0]))
            self.assertEqual(chunk.read(), self.STRINGS[1])

    def test_eof(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[2]) + 1,
                               len(self.STRINGS[0]) + len(self.STRINGS[1]))
            with self.assertRaises(EOFError):
                chunk.read()
            chunk.seek(0)
            self.assertEqual(chunk.read(chunk.size - 1), self.STRINGS[2])
            with self.assertRaises(EOFError):
                chunk.read(1)

    def test_closed(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[0]))
            self.assertFalse(chunk.closed)
        self.assertTrue(chunk.closed)
        with self.assertRaises(ValueError):
            chunk.read()

    def test_seek(self):
        with self.get_raw_buffer() as data_file:
            chunk = RawIOChunk(data_file, len(self.STRINGS[1]),
                               len(self.STRINGS[0]))
            self.assertEqual(chunk.seek(1), 1)
            self.assertEqual(chunk.tell(), 1)
            self.assertEqual(chunk.seek(1, SEEK_CUR), 2)
            self.assertEqual(chunk.tell(), 2)
            self.assertEqual(chunk.seek(-1, SEEK_END),
                             len(self.STRINGS[1]) - 1)
            self.assertEqual(chunk.tell(), len(self.STRINGS[1]) - 1)
            self.assertEqual(chunk.seek(0), 0)
            self.assertEqual(chunk.read(), self.STRINGS[1])
            self.assertEqual(chunk.seek(0), 0)
            self.assertEqual(chunk.read(), self.STRINGS[1])

    def test_full_file(self):
        with self.get_raw_buffer() as data_file:
            chunks = [RawIOChunk(data_file, len(self.STRINGS[0]))]
            chunks.append(RawIOChunk(data_file, len(self.STRINGS[1]),
                                     chunks[0].end))
            chunks.append(RawIOChunk(data_file, len(self.STRINGS[2]),
                                     chunks[1].end))
            self.assertEqual(sum(chunk.size for chunk in chunks),
                             len(b''.join(self.STRINGS)))
