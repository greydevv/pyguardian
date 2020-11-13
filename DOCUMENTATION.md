# pyguard docs

## Getting started
Currently, pyguard is still in development but will be made available on the Python Packaging Index in the future.

## Usage

To access the guard decorator, it must be imported first:
```python
from pyguard import guard
```

## Contents
- [guard](https://github.com/greysonDEV/pyguard/blob/master/DOCUMENTATION.md#guard)
- [ArgumentIncongruityWarning](https://github.com/greysonDEV/pyguard/blob/master/DOCUMENTATION.md#argumentincongruitywarning)
- [InvalidArgumentError](https://github.com/greysonDEV/pyguard/blob/master/DOCUMENTATION.md#invalidargumenterror)

### guard

The guard decorator's signature is as follows:
```python
@guard(*types, **kwtypes)
```
The constructor only accepts items of type `type` and `tuple`. If a `tuple` is passed, it must also only contain items of type `type`. If illegal values are passed to the constructor, a `ValueError` is raised with the message:
```
guard constructor not properly called!
```
The method below, `foo`, only takes one parameter `x`. By passing `int` into the guard decorator, it will force `x` to be of type `int`.
```python
@guard(int)
def foo(x):
	...
```
Multiple types for one parameter may also be specified by passing a `tuple`:
```python
@guard((int, float))
def foo(x):
	...

foo(1)   # valid call
foo(1.2) # valid call
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

Guarding functions that take an arbitrary number of parameters, i.e. `*args` and `**kwargs`, works almost identically to specifying types for other parameters. The obvious difference is that the unpacking operator, `*`/`**`, should not be passed to the guard decorator when specifying types via keyword.
```python
@guard(args=int)
def foo(*args, **kwargs):
	...

foo(1, 2)    # valid call
foo(1, True) # invalid call

@guard(kwargs=int)
def foo(**kwargs):
	...

foo(a="Hello", b="World") # valid call
foo(a=1, b="World")       # invalid call
```

### ArgumentIncongruityWarning

If there is an incongruence in the number of enforced types and parameters, an `ArgumentIncongruityWarning` will appear:
```python
@guard(int, str)
def foo(x):
	...
```
```
Enforcing 2 types while only 1 argument exists. 
```
```python
@guard(int)
def foo(x, y):
	...
```
```
Enforcing only 1 type while 2 arguments exist. Defined method, 'foo,' may produce unexpected results.
```
Warnings may be silenced via the `warning` module:
```python
import warnings

warnings.filterwarnings("ignore")
```

### InvalidArgumentError

If a value of type `int` is passed to the guarded method, `foo`, the method will execute normally. If a value not of type `int` is passed, i.e. `str`, an `InvalidArgumentError` is raised:
```python
@guard(int)
def foo(x):
	...

foo(1)   # valid call
foo("a") # invalid call
```
```
'foo' expects parameter 'x' to be of type 'int' but found 'str'
```