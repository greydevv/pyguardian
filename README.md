# pyguardian

## Description
*pyguardian* is a type-checker for method parameters. Methods are type-checked at runtime via the `guard` decorator:
```python
from pyguardian import guard

@guard(int, int)
def add(a, b):
    return a+b

# Successful call
>>> add(1,2)
3

# Unsccessful call ("2" is not an integer!)
>>> add(1,"2")
InvalidArgumentTypeError: 'add' expects value of type 'int' for parameter 'b' but got 'str'
```

## Installation
```bash
pip install pyguardian
```

## Documentation
See [DOCUMENTATION.md](https://github.com/greysonDEV/pyguardian/blob/master/DOCUMENTATION.md)

## License
*pyguardian* is licensed under the [MIT](https://github.com/greysonDEV/pyguardian/blob/master/LICENSE) License.
