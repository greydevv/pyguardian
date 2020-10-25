class ArgumentIncongruityWarning(Warning):
	"""
	ArgumentIncongruityWarning (subclass of Warning) is raised when number 
	of type arguments do not match the function's number of parameters. 
	This could mean both enforcing more types than there are parameters, or 
	vice versa.
	"""
	def __init__(self, funcname, typecount, argcount):
		if typecount > argcount:
			self.msg = (
			f"Enforcing {typecount} {'type' if typecount == 1 else 'types'} "
			f"while only {argcount} {'argument exists' if argcount == 1 else 'arguments exist'}. "
			)
		elif typecount < argcount:
			self.msg = (
			f"Enforcing only {typecount} {'type' if typecount == 1 else 'types'} "
			f"while {argcount} {'argument exists' if argcount == 1 else 'arguments exist'}. "
			f"Defined method, {funcname}(), may produce unexpected results."
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