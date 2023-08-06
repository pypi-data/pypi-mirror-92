# nonemptystr

[![PyPI](https://img.shields.io/pypi/v/nonemptystr)](https://pypi.org/project/nonemptystr/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonemptystr)](https://pypi.org/project/nonemptystr/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/nekonoshiri/nonemptystr)](https://github.com/nekonoshiri/nonemptystr/blob/main/LICENSE)

Non-empty string.

## Usage

```Python
from nonemptystr import EmptyString, nonemptystr

name: nonemptystr = nonemptystr("John")

try:
    name = nonemptystr("")
except EmptyString:
    print("The name is empty.")
```

## API

### Module `nonemptystr`

#### *class* `nonemptystr(obj: object)`

Subclass of `str`.
Raise `EmptyString` exception if `str(obj)` is empty string.

#### *class* `EmptyString`

Subclass of `ValueError`.

