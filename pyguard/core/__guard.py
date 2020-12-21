import warnings
import inspect
from functools import wraps
from pyguard.errors import ArgumentIncongruityWarning, InvalidArgumentError, UnknownKeywordArgumentWarning
from pyguard.core.all_instance import all_instance
from pyguard.core.find_illegal import find_illegal
from pyguard.core.__sig import get_param_kinds

class Guard:
	def __init__(self, *types, **kwtypes):
		"""
		See '__validate_constructor' for examples of valid and invalid inputs. 
		"""
		self.types = self.__replace_none(types)
		self.kwtypes = self.__replace_none(kwtypes)
		self.__validate_constructor()

	def __call__(self, func):
		"""
		'__call__' is implemented to allow the Guard decoration of methods and 
		is therefore called when the decorated method is called.
		"""
		self.func = func
		@wraps(func)
		def decor(*args, **kwargs):
			sig = inspect.signature(func)
			argu = sig.bind(*args, **kwargs)
			argu.apply_defaults()

			passed_values = argu.arguments
			enforced_types = self.__apply_types(passed_values)
			param_kinds = get_param_kinds(sig)

			compiled_params = []
			for param in passed_values:
				if enforced_types[param] is not None:
					compiled_param = {
						"name": param,
						"value": passed_values[param],
						"enforced_type": enforced_types[param],
						"kind": param_kinds[param]
					}
					compiled_params.append(compiled_param)

			self.__validate_func(compiled_params)

			return func(*args, **kwargs)
		return decor

	@staticmethod
	def __replace_none(iterable):
		"""
		Replaces instances of 'None' with 'NoneType' in the iterable argument. 
		Instances of 'None' that are contained inside a nested iterable are also replaced.

		Parameters:
		iterable -- the iterable containing 'None'

		Examples:
		>>> __replace_none((str, None))
		(str, NoneType)

		>>> __replace_none((str, (int, None)))
		(str, (int, NoneType))
		"""
		if isinstance(iterable, dict):
			for idx, (name, classinfo) in enumerate(iterable.items()):
				if isinstance(classinfo, (list, tuple)) and None in classinfo:
					iterable[name] = tuple(type(None) if t is None else t for t in classinfo)
		else:
			for idx, classinfo in enumerate(iterable):
				if isinstance(classinfo, (list, tuple)) and None in classinfo:
					iterable[idx] = tuple(type(None) if t is None else t for t in classinfo)
				elif classinfo is None:
					iterable[idx] = type(None)
		return iterable

	@staticmethod
	def __allinstance(iterable, classinfo, return_illegal=False):
		"""
		'__allisntance' is responsible for scanning the elements of an iterable and verifying that all of those elements are of the specified type.
		
		Parameters:
		iterable       -- the iterable to scan
		classinfo      -- the type or class to check against
		return_illegal -- if True, the first element that is not an instance or direct/virtual subclass of is additionally returned

		Examples:
		>>> __allinstance([1, 2, 3], int, False)
		True
		
		>>> __allinstance([1, 2, 3], int, True)
		True, None

		>>> __allinstance([1, 2.1, 3], int, True)
		False, 2.1
		"""
		if return_illegal:
			for e in iterable:
				if not isinstance(e, classinfo):
					return False, e
			return True, None
		else:
			return all(isinstance(e, classinfo) for e in iterable)

	def __apply_types(self, passed_values):
		"""
		'__apply_types' is implemented for format the arguments and parameters in 
		a way that allows other methods to use the data easily and efficiently. 
		A dictionary is returned with the method's parameters as the keys 
		and the enforced type on each of those parameters as the value.
		"""
		type_count = len(self._types) + len(self._kwtypes)
		param_count = len(passed_values)
		if type_count != param_count:
			warnings.warn(
				ArgumentIncongruityWarning(
					func = self.func,
					type_count = type_count,
					param_count = param_count
				),
				stacklevel = 3
			)

		applied = {k:None for k in passed_values}
		# apply keywords first
		unknowns = []
		for param in self._kwtypes.keys():
			if passed_values.get(param):
				applied[param] = self._kwtypes[param]
			else:
				unknowns.append(param)

		if len(unknowns) > 0:
			warnings.warn(
				UnknownKeywordArgumentWarning(
					func = self.func,
					unknown_keywords = unknowns
				),
				stacklevel = 3
			)

		# apply types to rest, from left to right
		idx = 0
		for k in applied.keys():
			if idx > len(self._types)-1:
				break
			if applied[k] is None:
				applied[k] = self._types[idx]
				idx += 1

		return applied

	def __validate_func(self, compiled_params):
		"""
		'__validate_func' is implemented to validate the types of the parameters 
		passed to the method against the enforced types passed to the Guard 
		constructor. 
		
		Examples
		--------

		If the types of the parameters passed to the method do not match their 
		enforced type, an exception is raised: "InvalidArgumentError: 'foo' 
		expects parameter "c" to be of type "int" but found "str""

		>>> @guard(int, int, int)
		>>> def foo(a, b, c):

		>>> foo(1, 2, 'Hello World!')

		"""
		for param in compiled_params:
			if param["kind"] in ["VAR_POSITIONAL", "VAR_KEYWORD"]: # *args or **kwargs, parse tuple or dict respectively
				illegal_type = find_illegal(param["value"], param["enforced_type"])
				if illegal_type:
					raise(InvalidArgumentError(
						func = self.func, 
						param_name = param["name"], 
						enforced_type = param["enforced_type"], 
						passed_type = illegal_type
					))
			else:
				if not isinstance(param["value"], param["enforced_type"]):
					raise(InvalidArgumentError(
						func = self.func, 
						param_name = param["name"], 
						enforced_type = param["enforced_type"], 
						passed_type = type(param["value"])
					))

	def __validate_constructor(self):
		"""
		'__validate_constructor' is implemented to validate the passed *types 
		and **kwtypes of the Guard class.

		Parameters
		----------
		*types   : type, (type,)
		**kwtypes: type, (type,)


		Examples
		--------
		
		Parameters 'a', 'b', and 'c' must be of type 'int', 'int', and 'int', 
		respectively.

		>>> @guard(int, int, int)
		>>> def foo(a, b, c):

		>>> foo(1, 2, 3)



		A tuple filled with elements of type 'type' passed signifies multiple 
		valid types for one parameter. In this case, parameter 'c' can either 
		be of type 'int' or 'float.'

		>>> @guard(int, int, (int, float))
		>>> def foo(a, b, c):

		>>> foo(1, 2, 3)
		>>> foo(1, 2, 3.14159)
	
	

		Types passed via keyword is also accepted, given that the keyword 
		matches the name of a parameter that exists in the method's signature.

		>>> @guard(a=int, b=int, c=int)
		>>> def foo(a, b, c):

		>>> foo(1, 2, 3)
		


		Similarly to the last example, a combination of both positional and 
		keyworded arguments are able to be passed into the Guard constructor 
		and will also support out-of-order type-enforcement. In this example, 
		'a=str' enforces that the method's parameter 'a' must be of type 'str', 
		even though it was specified as a keyword argument that follows 
		multiple positional arguments. Both 'b' and 'c' will then be enforced 
		to be of type 'int.'

		>>> @guard(int, int, a=str):
		>>> def foo(a, b, c):

		>>> foo('Hello World!', 1, 2)



		Only types and tuples of types may be passed to the constructor.	
		When called, this method will raise an exception: "ValueError: guard 
		constructor not properly called!"

		>>> @guard(int, int, 'foo')
		>>> def foo(a, b, c):

		>>> foo(1, 2, 3)



		A warning will be raised when the number of types passed to the Guard 
		constructor is larger than the number of parameters in the method's 
		signature. When the method is called, this warning is raised: 
		"ArgumentIncongruityWarning: Enforcing 4 types while only 3 arguments 
		exist."

		>>> guard(int, int, int, str)
		>>> def foo(a, b, c):

		>>> foo(1, 2, 3)



		Similarly to the last example, a warning will be raised when the number 
		of parameters in the method's signature is larger than the number of 
		types passed to the Guard constructor. When the method is called, this 
		warning is raised: "ArgumentIncongruityWarning: Enforcing only 3 types 
		while 4 arguments exist. Defined method, 'foo,' may produce unexpected 
		results."

		>>> guard(int, int, int)
		>>> def foo(a, b, c, d):

		>>> foo(1, 2, 3, 4)

		"""
		all_types = list(self._types) + list(self._kwtypes.values())
		
		for enforced_type in all_types:
			if not isinstance(enforced_type, (type, tuple)) and enforced_type is not None:
				raise(ValueError(f"guard constructor not properly called!"))
			elif isinstance(enforced_type, tuple):
				if not all_instance(enforced_type, type) or len(enforced_type) == 0:
					raise(ValueError(f"guard constructor not properly called!"))