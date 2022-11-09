"""
These tests are aimed to ensure that the `RawIOChunk` instances behave consistently with
the other `RawIOBase` implementations.
"""

import os
from contextlib import nullcontext as does_not_raise
from dataclasses import dataclass
from io import SEEK_CUR, SEEK_END, BufferedIOBase, BytesIO, RawIOBase
from itertools import product
from tempfile import TemporaryFile
from typing import IO, Any, Callable, ContextManager

import pytest

from io_chunks.raw_io_chunk import RawIOChunk

IOFactory = Callable[[], IO]


def temp_file_factory(contents: bytes, buffering=-1) -> IO:
    temp_file = TemporaryFile("w+b", buffering=buffering)
    temp_file.write(contents)
    temp_file.seek(0)
    return temp_file


@dataclass(frozen=True)
class UseCase:
    """
    Represent a supported use case to check compatibility with the `RawIOBase` or to
    verify it.
    Contains all the results and expectations of all the tests.

    This allows to have all the use case definitions in a single place.
    """

    factory: IOFactory
    name: str
    size: int
    full_read_result: bytes
    negative_seek_expect: ContextManager[Any]
    before_start_seek_expect: ContextManager[Any]
    seek_hole_expect: ContextManager[Any]
    seek_data_expect: ContextManager[Any]
    truncate_negative_expect: ContextManager[Any]


@dataclass(frozen=True)
class ClosedAction:
    """
    The secondary part of the use cases for the `test_closed_raises_value_error`
    """

    action: Callable[[IO], Any]
    name: str


USE_CASES = [
    UseCase(
        factory=lambda: BytesIO(b"01234"),
        name="BytesIO",
        size=5,
        full_read_result=b"01234",
        negative_seek_expect=pytest.raises(ValueError),
        before_start_seek_expect=does_not_raise(),
        seek_hole_expect=pytest.raises(ValueError),
        seek_data_expect=pytest.raises(ValueError),
        truncate_negative_expect=pytest.raises(ValueError),
    ),
    UseCase(
        factory=lambda: RawIOChunk(BytesIO(b"01234"), size=4),
        name="RawIOChunk (size 4)",
        size=4,
        full_read_result=b"0123",
        negative_seek_expect=pytest.raises(ValueError),
        before_start_seek_expect=does_not_raise(),
        seek_hole_expect=pytest.raises(ValueError),
        seek_data_expect=pytest.raises(ValueError),
        truncate_negative_expect=pytest.raises(ValueError),
    ),
    UseCase(
        factory=lambda: RawIOChunk(BytesIO(b"01234"), size=5),
        name="RawIOChunk (size 5)",
        size=5,
        full_read_result=b"01234",
        negative_seek_expect=pytest.raises(ValueError),
        before_start_seek_expect=does_not_raise(),
        seek_hole_expect=pytest.raises(ValueError),
        seek_data_expect=pytest.raises(ValueError),
        truncate_negative_expect=pytest.raises(ValueError),
    ),
    UseCase(
        factory=lambda: RawIOChunk(BytesIO(b"01234"), size=6),
        name="RawIOChunk (size 6)",
        size=6,
        full_read_result=b"01234",
        negative_seek_expect=pytest.raises(ValueError),
        before_start_seek_expect=does_not_raise(),
        seek_hole_expect=pytest.raises(ValueError),
        seek_data_expect=pytest.raises(ValueError),
        truncate_negative_expect=pytest.raises(ValueError),
    ),
    UseCase(
        factory=lambda: temp_file_factory(b"01234"),
        name="TempFile",
        size=5,
        full_read_result=b"01234",
        negative_seek_expect=pytest.raises(OSError),
        before_start_seek_expect=pytest.raises(OSError),
        seek_hole_expect=does_not_raise(),
        seek_data_expect=does_not_raise(),
        truncate_negative_expect=pytest.raises(OSError),
    ),
    UseCase(
        factory=lambda: temp_file_factory(b"01234", buffering=0),
        name="TempFile (unbuffered)",
        size=5,
        full_read_result=b"01234",
        negative_seek_expect=pytest.raises(OSError),
        before_start_seek_expect=pytest.raises(OSError),
        seek_hole_expect=does_not_raise(),
        seek_data_expect=does_not_raise(),
        truncate_negative_expect=pytest.raises(OSError),
    ),
]

CLOSED_ACTIONS = [
    ClosedAction(lambda buffer: buffer.read(), name="read"),
    ClosedAction(lambda buffer: buffer.seek(0), name="seek"),
    ClosedAction(lambda buffer: buffer.tell(), name="tell"),
    ClosedAction(lambda buffer: buffer.seekable(), name="seekable"),
    ClosedAction(lambda buffer: buffer.readable(), name="readable"),
]

use_cases_param = pytest.mark.parametrize(
    "use_case", USE_CASES, ids=lambda param: param.name
)


@use_cases_param
def test_full_read(use_case: UseCase):
    with use_case.factory() as instance:
        result = instance.read()
        assert result == use_case.full_read_result
        assert instance.read() == b""
        assert instance.read(1) == b""


@pytest.mark.parametrize(
    ["use_case", "action"],
    product(USE_CASES, CLOSED_ACTIONS),
    ids=lambda param: param.name,
)
def test_closed_raises_value_error(use_case: UseCase, action: ClosedAction):
    with use_case.factory() as instance:
        assert instance.closed is False
        action.action(instance)
        instance.close()
        assert instance.closed is True
        with pytest.raises(ValueError):
            action.action(instance)


@use_cases_param
def test_closed_values(use_case: UseCase):
    with use_case.factory() as instance:
        assert instance.tell() == 0
        assert instance.seek(0) == 0
        assert instance.readable() is True
        assert instance.seekable() is True


@use_cases_param
def test_extra_seek(use_case: UseCase):
    with use_case.factory() as instance:
        assert instance.seek(100) == 100
        assert instance.tell() == 100


@use_cases_param
def test_negative_seek(use_case: UseCase):
    with use_case.factory() as instance:
        with use_case.negative_seek_expect:
            instance.seek(-1)


@use_cases_param
def test_seek_inside(use_case: UseCase):
    with use_case.factory() as instance:
        assert instance.seek(0) == 0
        assert instance.seek(1) == 1


@use_cases_param
def test_seek_outside(use_case: UseCase):
    with use_case.factory() as instance:
        assert instance.seek(10) == 10


@use_cases_param
def test_seek_end_inside(use_case: UseCase):
    with use_case.factory() as instance:
        assert instance.seek(-1, SEEK_END) == use_case.size - 1


@use_cases_param
def test_seek_end_outside(use_case: UseCase):
    with use_case.factory() as instance:
        with use_case.before_start_seek_expect:
            assert instance.seek(-10, SEEK_END) == 0


@use_cases_param
def test_seek_cur_inside(use_case: UseCase):
    with use_case.factory() as instance:
        assert instance.seek(1) == 1
        assert instance.seek(1, SEEK_CUR) == 2
        assert instance.seek(-1, SEEK_CUR) == 1
        assert instance.seek(-1, SEEK_CUR) == 0


@use_cases_param
def test_seek_cur_ouside(use_case: UseCase):
    with use_case.factory() as instance:
        with use_case.before_start_seek_expect:
            assert instance.seek(-1, SEEK_CUR) == 0


@use_cases_param
def test_seek_hole(use_case: UseCase):
    with use_case.factory() as instance:
        with use_case.seek_hole_expect:
            instance.seek(0, os.SEEK_HOLE) == 0


@use_cases_param
def test_seek_data(use_case: UseCase):
    with use_case.factory() as instance:
        with use_case.seek_hole_expect:
            instance.seek(0, os.SEEK_DATA) == 3


@use_cases_param
def test_pos_invalid_type(use_case: UseCase):
    with use_case.factory() as instance:
        with pytest.raises(TypeError):
            instance.seek("a")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            instance.seek(1, "a")  # type: ignore[arg-type]


@use_cases_param
def test_readinto_empty_array(use_case: UseCase):
    with use_case.factory() as instance:
        # readinto is not in IO or IOBase but in RawIOBase and BufferedIOBase.
        # While this test is not part of the IO contract, it *is* part of the RawIOBase
        # contract, the class RawIOChunk inherits.
        assert isinstance(instance, (RawIOBase, BufferedIOBase))
        buffer = bytearray(0)
        assert instance.readinto(buffer) == 0
        assert buffer == b""


@use_cases_param
def test_truncate(use_case: UseCase):
    with use_case.factory() as instance:
        assert instance.truncate(2) == 2
        assert instance.read() == b"01"


@use_cases_param
def test_truncate_negative(use_case: UseCase):
    with use_case.factory() as instance:
        with use_case.truncate_negative_expect:
            assert instance.truncate(-1) == 0
