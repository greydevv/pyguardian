class ArgumentIncongruityWarning(Warning):
	"""
	ArgumentIncongruityWarning (subclass of Warning) is raised when number 
	of type arguments do not match the function's number of parameters. 
	This could mean both enforcing more types than there are parameters, or 
	less types than there are parameters.
	"""
	def __init__(self, func_name, type_count, arg_count):
		if type_count > arg_count:
			self.msg = (
			f"Enforcing {type_count} {'type' if type_count == 1 else 'types'} "
			f"while only {arg_count} {'argument exists' if arg_count == 1 else 'arguments exist'}. "
			)
		elif type_count < arg_count:
			self.msg = (
			f"Enforcing only {type_count} {'type' if type_count == 1 else 'types'} "
			f"while {arg_count} {'argument exists' if arg_count == 1 else 'arguments exist'}. "
			f"Defined method, {func_name}(), may produce unexpected results."
			)

	def __str__(self):
		return self.msg

class InvalidArgumentError(TypeError):
	"""
	InvalidArgumentError (subclass of TypeError) is raised when the type of 
	a value passed to a guarded method does not match the enforced type.
	"""
	def __init__(self, func, param, enforced_type, given_type):
		enforced_type = self.__create_str(enforced_type)
		self.error = (
			f"'{func.__qualname__}' expects parameter '{param}' to be of type {enforced_type} but found '{given_type}'"
		)

	def __create_str(self, x):
		if isinstance(x, tuple):
			x = [i.__name__ for i in x]
			if len(x) == 1:
				return f"'{x[0]}'"
			elif len(x) == 2:
				return f"'{x[0]}' or '{x[1]}'"
			else:
				listed = ",' ".join([f"'{i}" for i in x[0:-1]])
				return f"{listed},' or '{x[-1]}'"
		else:
			return f"'{x.__name__}'"

	def __str__(self):
		return self.error