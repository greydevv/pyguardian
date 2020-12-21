class InvalidArgumentTypeError(TypeError):
	"""
	Raised when a value of an incorrect type is passed to a guarded function.
	Subclass of 'TypeError'

	Parameters:
	func        -- the guarded function
	param_name  -- the name of the parameter that received an incorrectly-typed value
	classinfo   -- the type or class that was enforced
	passed_type -- the incorrect type
	"""
	def __init__(self, func, param_name, classinfo, passed_type):
		classinfo = self.__make_readable(classinfo)
		self.err_msg = f"'{func.__qualname__}' expects value of type {classinfo} for parameter '{param_name}' but got '{passed_type.__name__}'"

	@staticmethod
	def __make_readable(classinfo):
		if isinstance(classinfo, (list, tuple)):
			if len(classinfo) == 1:
				return f"'{classinfo[0].__name__}'"
			elif len(classinfo) == 2:
				return f"'{classinfo[0].__name__}' or '{classinfo[1].__name__}'"
			else:
				listed = ", ".join(f"'{t.__name__}'" for t in classinfo[0:-1])
				return f"{listed}, or '{classinfo[-1].__name__}'"
		else:
			return f"'{classinfo.__name__}'"

	def __str__(self):
		return self.err_msg

class UnknownKeywordArgumentWarning(Warning):
	"""
	Raised when a the guard constructor receives a keyword argument that does not exist in the guarded method's signature.
	Subclass of 'Warning'

	Parameters:
	func             -- the guarded function
	unknown_keywords -- the keywords that do not exist in the guarded method's signature
	"""
	def __init__(self, func, unknown_keywords):
		plural = len(unknown_keywords) > 1
		unknown_keywords = self.__make_readable(unknown_keywords)
		self.wrn_msg = f"guard constructor received unknown keyword {'arguments' if plural else 'argument'} {unknown_keywords} which may produce unexpected results as {'these arguments' if plural else 'this argument'} will not be applied."

	@staticmethod
	def __make_readable(kwds):
		if isinstance(kwds, (list, tuple)):
			if len(kwds) == 1:
				return f"'{kwds[0]}'"
			elif len(kwds) == 2:
				return f"'{kwds[0]}' and '{kwds[1]}'"
			else:
				listed = ", ".join(f"'{t}'" for t in kwds[0:-1])
				return f"{listed}, and '{kwds[-1]}'"
		else:
			return f"'{kwds}'"

	def __str__(self):
		return self.wrn_msg