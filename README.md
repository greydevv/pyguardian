# pyguardian

## Description
*pyguardian* is a type-checker for method parameters. Methods are type-checked at runtime via the `guard` decorator:
```python
from pyguardian import guard

@guard(int, int)
def add(a, b):
    return a+b

>>> add(1,2)
3
>>> add(1,"2")
pyguardian.errors.InvalidArgumentTypeError: 'add' expects value of type 'int' for parameter 'b' but got 'str'
```

## Installation
```bash
pip install pyguardian
```

## Documentation
[DOCUMENTATION.md](https://github.com/greysonDEV/pyguardian/blob/master/DOCUMENTATION.md)

## License
*pyguardian* is licensed under the [MIT](https://github.com/greysonDEV/pyguardian/blob/master/LICENSE) License.
