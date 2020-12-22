# pyguardian docs

## Getting started
To download pyguardian, run this command from the console:
```bash
pip install pyguardian
```

## Contents
- [Usage](https://github.com/greysonDEV/pyguardian/blob/main/DOCUMENTATION.md#usage)
- [guard](https://github.com/greysonDEV/pyguardian/blob/main/DOCUMENTATION.md#guard)
- [UnknownKeywordArgumentWarning](https://github.com/greysonDEV/pyguardian/blob/main/DOCUMENTATION.md#unknownkeywordargumentwarning)
- [InvalidArgumentTypeError](https://github.com/greysonDEV/pyguardian/blob/main/DOCUMENTATION.md#invalidargumenttypeerror)

### Usage

To access the guard decorator, it must be imported first:
```python
from pyguardian import guard
```

### guard

The guard decorator's signature is as follows:
```python
@guard(*types, **kwtypes)
```
The constructor accepts items of type `type`, `NoneType` and `list`/`tuple` containing elements of type `type`. If an invalid argument is passed to the constructor, a `ValueError` is raised with the message:
```
guard constructor not properly called!
```
The method below takes one parameter, `x`. By passing `int` to the guard decorator, `x` now only accepts a value of type `int`.
```python
@guard(int)
def foo(x):
    ...

foo(1)             # valid call
foo("Hello World") # invalid call
```
Multiple types for one parameter may also be specified by passing a `list` or a `tuple` containing elements of type `type`:
```python
@guard((int, float))
def foo(x):
    ...

foo(1)   # valid call
foo(1.2) # valid call
```
By not enforcing a type on a parameter, that parameter will then accept a value of any type.
```python
@guard(int)
def foo(x, y):
    ...

foo(1, "Hello World") # valid call
foo(1, True)          # valid call
```
Note that the below is also accepted but not encouraged as the constructor accepts `None` by itself.
```python
@guard((int, type(None)))
def foo(x):
    ...
```
When guarding methods defined inside of a class, `object` must be the first argument passed to the guard decorator for instance and class methods. `object` does not need to be passed to static methods.
```python
class Foo:
    @guard(object, int)
    def __init__(self, x):
        ...

    @guard(object, str)
    def bar(self, x):
        ...

    @classmethod
    @guard(object, float)
    def baz(cls, x):
        ...

    @staticmethod
    @guard(list)
    def qux(x):
        ...
```
Guarding functions with parameters that take an arbitrary amount of arguments, i.e. `*args` and `**kwargs`, works identically to specifying types for other parameters. The obvious difference is that the unpacking operator (`*`/`**`) should not be passed to the guard decorator when specifying types via keyword.
```python
@guard(args=int)
def foo(*args):
    ...

foo(1, 2)    # valid call
foo(1, True) # invalid call

@guard(kwargs=int)
def foo(**kwargs):
    ...

foo(a="Hello", b="World") # valid call
foo(a=1, b="World")       # invalid call

@guard(int, str)
def foo(*args, **kwargs):
    ...

foo(1, 2, a="Hello", b="World") # valid call
foo(1, 2, a="Hello", b=1.2)     # invalid call
```

### UnknownKeywordArgumentWarning

`UnknownKeywordArgumentWarning` is a subclass of `Warning`.

If there is an unknown keyword passed to the guard decorator, an `UnknownKeywordArgumentWarning` is raised:
```python
@guard(y=int)
def foo(x):
    ...
```
```
UnknownKeywordArgumentWarning: guard constructor received unknown keyword argument 'y' which may produce unexpected results as this argument will not be applied.
```

```python
import warnings

warnings.filterwarnings("ignore")
```

### InvalidArgumentTypeError

`InvalidArgumentTypeError` is a subclass of `TypeError`.

If a value of type `int` is passed to the guarded method, `foo`, the method will execute normally. If a value not of type `int` is passed, i.e. `str`, an `InvalidArgumentError` is raised:
```python
@guard(int)
def foo(x):
    ...

foo(1)   # valid call
foo("a") # invalid call
```
```
InvalidArgumentTypeError: 'foo' expects value of type 'int' for parameter 'x' but got 'str'
```