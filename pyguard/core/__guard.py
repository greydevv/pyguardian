import inspect
import warnings
from functools import wraps
from pyguard.errors import ArgumentIncongruityWarning

class Guard():
	def __init__(self, *types, **kwtypes):
		self.types = types
		self.kwtypes = kwtypes

	def __call__(self, func):
		@wraps(func)
		def inner(*args, **kwargs):
			sig = inspect.signature(func)
			argspec = inspect.getfullargspec(func)
			print({k:v for k,v in zip(argspec.args, list(args))})
			# print([param for param in sig.parameters.items()])
			print({p:None for p, k in sig.parameters.items()})
			# passedargs = dict(zip(inspect.getfullargspec(func).args, list(args)))
			# passedargs = dict(zip(inspect.signature(func)))
			# print(passedargs)

			# scannedargs = self.__scanargs(passedargs)
			# argcount = len(list(self.types) + list(self.kwtypes.items()))
			# print(self.__validate(scannedargs, passedargs))

			return func(*args, **kwargs)
		return inner

	def __validate(self, scannedargs, passedargs):
		specified = {a:t for a,t in scannedargs.items() if t is not None}
		for a,t in specified.items():
			if isinstance(t, (list, tuple)):
				if not isinstance(passedargs[a], tuple(t)):
					return False
			else:
				if not isinstance(passedargs[a], t):
					return False
		return True

	def __scanargs(self, passedargs):
		matched = (passedargs.keys() & self.kwtypes.keys())
		scannedargs = {k:None for k in passedargs}
		# scan for keywords first
		for k in passedargs:
			if k in matched:
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



# if argcount != len(passedargs):
			# 	msg = (
			# 		f"Enforcing {argcount} type(s) "
			# 		f"while {len(passedargs)} arguments exist."
			# 	)
			# 	warnings.warn(
			# 		msg,
			# 		ArgumentIncongruityWarning,
			# 		stacklevel=2
			# 	)