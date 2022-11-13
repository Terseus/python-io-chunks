# io-chunks

> _Man, I wish there was a way to split this opened file into smaller subfiles to read any part of it independently!_
>
> -- No one ever

I made a library for it anyway.

## What's this?

This library contains utilities (well, _one_ utility) to get a Python buffer from another buffer, allowing you to read from each of them separately.

Let me show you an example.

```python
from io_chunks import RawIOChunk

with open("test_file", "w") as file_handle:
    file_handle.write("Hello beautiful world!")

with open("test_file", "rb") as file_handle:
    # Create a "chunk" with the first 5 bytes
    chunk_hello = RawIOChunk(file_handle, 5)
    # Create a "chunk" starting at position 16 with the last 6 bytes
    chunk_world = RawIOChunk(file_handle, size=6, start=16)
    # This prints b'Hello'
    print(chunk_hello.read())
    # This prints b'world!'
    print(chunk_world.read())
    # Now, this prints b'Hello beautiful world!' to demostrate that the original
    # `file_handle` pointer wasn't altered at all!
    print(file_handle.read())
```

Amazing, right?

## Why?

While writing a parser I found this class to be somewhat useful, around 7 years ago.

While today I don't really see it today, I decided to clean it up and released it in case it's useful for someone.

## Install

Use `pip`:

```bash
$ pip install io-chunks
```

## Documentation

You can read it at [readthedocs](https://python-io-chunks.readthedocs.io/en/latest/).

## Run the tests

Create a venv with your favorite tool and activate it.
Then, install the development dependencies and execute `pytest`:

```bash
$ pip install -r requirements-dev.txt
$ pytest
```

Alternatively, to execute the tests using tox:

```bash
$ pip install tox
$ tox
```

## License

MIT
