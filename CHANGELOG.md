# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [2.0.0] - 2022-11-18

### Added

- Add isort, black, pre-commit.
- Add typing, mypy.
- Now `RawIOChunk` instances can be closed.
- Add `ClosedStreamError` exception, which inherits from `ValueError`.
- Now `RawIOChunk` instances can be used as a context manager.
- Implement `truncate` for `RawIOChunk`.
- Add tests to ensure that `RawIOChunk` behaves consistently with all the other
  Now `RawIOChunk` implements `IO` interface.
- Implement `IO` interface for `RawIOChunk`.
- Add `exceptions.py`.
- Add tox.

### Removed

- Remove Python 2 support.

### Changed

- Change `README.rst` to `README.md`.
- Replace `setup.py` with `pyproject.toml`.
- Renamed `chunks.py` to `raw_io_chunk.py`.
- Changed Sphinx doc to use Markdown with the [Myst parser](https://myst-parser.readthedocs.io/en/latest/).

### Fixed

- Now returns an empty bytes instead of raising `EOFError` when the underlying
  stream is empty.
- Raise `ValueError` when trying to seek at a negative position.
- Prevent to reach negative seek positions.
- Fix hardcoded values in some `ValueError` raised.
- Fix `flake8 .` scan the whole `.tox` and `build` directories.


## [1.0.2] - 2017-07-23

### Added

- Add automatic doc generation with Sphinx.
- Complete missing doc.
- Add this changelog.

### Changed

- Use `pytest` instead of `nose` for testing.


## [1.0.1] - 2017-06-03

### Added

- Initial public release.
- Class `RawIOChunk`.
