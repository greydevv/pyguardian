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
		all_types = list(self.types) + list(self.kwtypes)
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
















