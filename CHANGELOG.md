# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add isort, black, pre-commit.
- Add typing, mypy.
- Now `RawIOChunk` instances can be closed.
- Add `ClosedStreamError` exception, which inherits from `ValueError`.
- Now `RawIOChunk` instances can be used as a context manager.
### Removed
- Remove Python 2 support.
### Changed
- Change `README.rst` to `README.md`.
- Replace `setup.py` with `pyproject.toml`.
### Fixed
- Now returns an empty bytes instead of raising `EOFError` when the underlying
  stream is empty.

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
