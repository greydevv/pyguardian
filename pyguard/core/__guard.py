import warnings
from inspect import getfullargspec
from functools import wraps
from pyguard.errors import ArgumentIncongruityWarning, InvalidArgumentError

class Guard():
	def __init__(self, *types, **kwtypes):
		self.types = types
		self.kwtypes = kwtypes

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

	def __validate(self, scannedargs, passedargs):
		specified = {a:t for a,t in scannedargs.items() if t is not None}
		print(specified)
		for param,t in specified.items():
			# check if guard() is accepting multile types for one parameter
			if isinstance(t, list):
				# check if type is not of any of the types that were passed as a list
				
				# print(f"Found list: {str(list(t))}")
				if not isinstance(passedargs[param], tuple(t)):
					raise(InvalidArgumentError(param, [t.__name__ for t in t], type(param).__name__))
			else:
				if not isinstance(passedargs[param], t):
					raise(InvalidArgumentError(param, t.__name__, type(param).__name__))
				# print(f"Found singular: {str(t)}")
		return None

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
















