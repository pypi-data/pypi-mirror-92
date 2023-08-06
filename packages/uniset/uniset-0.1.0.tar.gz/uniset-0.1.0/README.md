[![Build Status](https://github.com/hukkinj1/uniset/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkinj1/uniset/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)
[![codecov.io](https://codecov.io/gh/hukkinj1/uniset/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/uniset)
[![PyPI version](https://img.shields.io/pypi/v/uniset)](https://pypi.org/project/uniset)

# uniset

> Pre-generated sets of Unicode code points

`uniset` is a module containing `frozenset`s of Unicode code points (characters).

## API

### Categories

The module includes a set for all Unicode categories and subcategories except the main category "C" (other)
and its subcategories "Co" (private use) and "Cn" (not assigned).

Example:

```python
import uniset

# The letter "A" is in category "L" (letters)
assert "A" in uniset.L
# The letter "A" is also in category "Lu" (uppercase letters)
assert "A" in uniset.Lu
```

### Whitespace

`uniset.WHITESPACE` contains all Unicode whitespace characters.
`uniset.WHITESPACE` is a union of ASCII whitespace characters and the Unicode category "Zs".

```python
import uniset

assert " " in uniset.WHITESPACE
```

### Punctuation

`uniset.PUNCTUATION` contains all Unicode punctuation letters.
`uniset.PUNCTUATION` is a union of ASCII punctuation characters and the Unicode category "P".

```python
import uniset

assert "." in uniset.PUNCTUATION
```

## Alternatives

[`unicategories`](https://gitlab.com/ergoithz/unicategories) also provides access to Unicode categories.
The implementation is based on "range groups" and iterators, and should be faster and more memory efficient than `uniset` for inclusion checks.

If you need the `frozenset` API (unions, intersections, etc.), or the sets beyond Unicode categories (whitespace, punctuation), use `uniset`.
Otherwise `unicategories` is the better option.
