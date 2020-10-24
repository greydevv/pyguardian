class ArgumentIncongruityWarning(Warning):
	"""
	Warning raised when number of type arguments do not match 
	the function's number of parameters. This could mean both
	overconstraining and underconstraining the method's parameters.
	"""