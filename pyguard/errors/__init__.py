class ArgumentIncongruityWarning(Warning):
	"""
	ArgumentIncongruityWarning (subclass of Warning) is raised when number 
	of type arguments do not match the function's number of parameters. 
	This could mean both enforcing more types than there are parameters, or 
	vice versa.
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
	def __init__(self, param, enforced_type, given_type):
		self.error = (
			f'Expected parameter "{param}" to be of type "{enforced_type}" but found "{given_type}"'
		)

	def __str__(self):
		return self.error