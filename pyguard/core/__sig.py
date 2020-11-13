from inspect import signature

def get_param_kinds(method_sig):
	return {name:str(param.kind) for name, param in method_sig.parameters.items()}