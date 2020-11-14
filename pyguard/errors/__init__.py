class ArgumentIncongruityWarning(Warning):
	"""
	'ArgumentIncongruityWarning' (subclass of Warning) is raised when number 
	of type arguments do not match the function's number of parameters. 
	This could mean both enforcing more or fewer types than there are 
	parameters.
	"""
	def __init__(self, func=None, type_count=None, param_count=None):
		if type_count > param_count:
			self.msg = (
			f"Enforcing {type_count} {'type' if type_count == 1 else 'types'} "
			f"while only {param_count} {'argument exists' if param_count == 1 else 'arguments exist'} "
			f"in defined method, '{func.__qualname__}.'"
			)
		elif type_count < param_count:
			self.msg = (
			f"Enforcing only {type_count} {'type' if type_count == 1 else 'types'} "
			f"while {param_count} {'argument exists' if param_count == 1 else 'arguments exist'}. "
			f"Defined method, '{func.__qualname__},' may produce unexpected results."
			)

	def __str__(self):
		return self.msg

class UnknownKeywordArgumentWarning(Warning):
	"""
	'UnknownKeywordArgumentWarning' (subclass of Warning) is raised when
	a type is enforced via keyword but does not exist in the defined
	method's signature.
	"""
	def __init__(self, func, unknown_keywords): 
		self.msg = (
			f"{'Argument' if len(unknown_keywords) == 1 else 'Arguments'} "
			f"{self.__create_str(unknown_keywords)} {'does' if len(unknown_keywords) == 1 else 'do'} "
			f"not exist in defined method, '{func.__qualname__}.' This may produce unexpected results."
		)

	@staticmethod
	def __create_str(x):
		if len(x) == 1:
				return f"'{x[0]}'"
		elif len(x) == 2:
			return f"'{x[0]}' and '{x[1]}'"
		else:
			listed = ",' ".join([f"'{i}" for i in x[0:-1]])
			return f"{listed},' and '{x[-1]}'"


	def __str__(self):
		return self.msg

class InvalidArgumentError(TypeError):
	"""
	'InvalidArgumentError' (subclass of TypeError) is raised when the type of 
	a value passed to a guarded method does not match the enforced type.
	"""
	def __init__(self, func, param_name, enforced_type, passed_type):
		enforced_type = self.__create_str(enforced_type)
		self.error = (
			f"'{func.__qualname__}' expects parameter '{param_name}' to be of type {enforced_type} but found '{passed_type.__name__}'"
		)

	@staticmethod
	def __create_str(x):
		if isinstance(x, tuple):
			x = [i.__name__ for i in x]
			if len(x) == 1:
				return f"'{x[0]}'"
			elif len(x) == 2:
				return f"'{x[0]}' or '{x[1]}'"
			else:
				listed = ",' ".join([f"'{i}" for i in x[0:-1]])
				return f"{listed},' or '{x[-1]},'"
		else:
			return f"'{x.__name__}'"

	def __str__(self):
		return self.error