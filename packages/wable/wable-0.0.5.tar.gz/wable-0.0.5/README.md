## Wable client

A client to communicate with wable.org api.

## Requirements

- [python > 3.7](https://www.python.org/downloads/release/python-370/)
- [pip](https://pip.pypa.io/en/stable/)

## Development

Clone the repository

```sh
pip install poetry
poetry install
```

To install a new python package

```sh
poetry add [NEW_PACKAGE]
```

To export poetry lock file to `requirements.txt` run

```sh
make deps
```

## Tests

```sh
make test
```

## Installation

The package is published at https://pypi.org/project/wable/

```sh
pip install wable
```

## Usage

```python
from wable.client import Wable

w = Wable()

# API to check if customer exists
exists = w.customer_exists(phone_number=123) # return True if phone number is registered else False

# more to come here
```
