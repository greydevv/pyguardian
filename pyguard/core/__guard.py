import warnings
from inspect import getfullargspec, signature
from functools import wraps
from pyguard.errors import ArgumentIncongruityWarning, InvalidArgumentError

class Guard():
	def __init__(self, *types, **kwtypes):
		self.types = types
		self.kwtypes = kwtypes
		self.__validate_constructor()

	def __call__(self, func):
		@wraps(func)
		def decor(*args, **kwargs):
			argspec = getfullargspec(func)
			passedargs = {k:v for k,v in zip(argspec.args, list(args))}
			scannedargs = self.__scanargs(passedargs)
			self.__validate(scannedargs, passedargs)

			typecount = len(list(self.types) + list(self.kwtypes))
			if typecount != len(argspec.args):
				warnings.warn(ArgumentIncongruityWarning(func.__name__, typecount, len(argspec.args)), stacklevel=2)

			return func(*args, **kwargs)
		return decor

	def __validate_constructor(self):
		"""
		__validate_constructor() is implemented to validate the passed *types and **kwtypes of 
		the Guard class. Valid types for the passed values of *types and **kwtypes are as follows:

		Parameters
		----------
		*types   : type, [type]
		**kwtypes: type, [type]

		Examples
		--------


		
		Parameters 'a', 'b', and 'c' must be of type 'int', 'int', and 'int', respectively.

		>>> @guard(int, int, int)
			def foo(a, b, c):

			foo(1, 2, 3)



		A list of 'type' passed signifies multiple valid types for one parameter. In this case, 
		parameter 'c' can either be of type 'int' or 'float.'

		>>> @guard(int, int, [int, float])
			def foo(a, b, c):

			foo(1, 2, 3)
			foo(1, 2, 3.14159)
	
	

		Types passed via keyword is also accepted, given that the keyword matches the name of
		a parameter that exists in the method's signature.

		>>> @guard(a=int, b=int, c=int)
			def foo(a, b, c):

			foo(1, 2, 3)
		


		Similarly to the last example, a combination of both positional and keyworded arguments 
		are able to be passed into the guard constructor and will also support out-of-order 
		type-enforcement. In this example, 'a=str' enforces that the method's parameter 'a' must be of 
		type 'str', even though it was specified as a keyword argument that follows multiple  
		positional arguments. Both 'b' and 'c' will then be enforced to be of type 'int.'

		>>> @guard(int, int, a=str):
			def foo(a, b, c):

			foo('Hello World!', 1, 2)



		Only types and lists of types may be passed to the constructor.	When called, this method will raise 
		an exception: "ValueError: guard constructor not properly called!"

		>>> @guard(int, int, 'foo')
			def foo(a, b, c):

			foo(1, 2, 3)



		A warning will be raised when the number of types passed to the guard constructor is larger 
		than the number of parameters in the method's signature. When the method is called, this warning 
		is raised: "ArgumentIncongruityWarning: Enforcing 4 types while only 3 arguments exist."

		>>> guard(int, int, int, str)
			def foo(a, b, c):

			foo(1, 2, 3)



		Similarly to the last example, a warning will be raised when the number of parameters in 
		the method's signature is larger than the number of types passed to the guard constructor.
		When the method is called, this warning is raised:
		"ArgumentIncongruityWarning: Enforcing only 4 types while 5 arguments exist. Defined method, 
		test(), may produce unexpected results."

		>>> guard(int, int, int)
			def foo(a, b, c, d):

			foo(1, 2, 3, 4)
		"""
		all_types = list(self.types) + list(self.kwtypes.values())
		for enforced_type in all_types:
			if not isinstance(enforced_type, (type, list)):
				raise(ValueError(f"guard constructor not properly called!"))
			elif isinstance(enforced_type, list):
				if not self.__allinstance(enforced_type, type):
					raise(ValueError(f"guard constructor not properly called!"))

	def __validate(self, scannedargs, passedargs):
		for param, enforced_type in scannedargs.items():
			if enforced_type is not None:
			# check if guard() is accepting multile types for one parameter
				if isinstance(enforced_type, list):
					# check if type is not of any of the types that were passed as a list
					if not isinstance(passedargs[param], tuple(enforced_type)):
						enforced_str = f"[{', '.join([t.__name__ for t in enforced_type])}]"
						raise(InvalidArgumentError(param, enforced_str, type(passedargs[param]).__name__))
				else:
					if not isinstance(passedargs[param], enforced_type):
						raise(InvalidArgumentError(param, enforced_type.__name__, type(passedargs[param]).__name__))

	def __scanargs(self, passedargs):
		specified_kw = (passedargs.keys() & self.kwtypes.keys())
		scannedargs = {k:None for k in passedargs}
		# scan for keywords first
		for k in passedargs:
			if k in specified_kw:
				scannedargs[k] = self.kwtypes[k]

		temp = list(self.types)
		for k in scannedargs:
			if scannedargs[k] is None:
				if len(temp) > 0:
					scannedargs[k] = temp[0]
					temp.remove(temp[0])
		return scannedargs

	def __allinstance(self, collection, valid_type):
		return all(isinstance(item, valid_type) for item in collection)
















