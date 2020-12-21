def list_to_string(lst):
	"""
	Creates a gramatically correct string from an lst.

	Parameters:
	lst -- the list that provides the elements for string construction

	Examples:
	>>> list_to_string(["apples", "oranges", "bananas"])
	"'apples', 'oranges', or 'bananas'"
	"""
	if isinstance(lst, (list, tuple)):
		if len(lst) == 1:
			return f"'{lst[0]}'"
		elif len(lst) == 2:
			return f"'{lst[0]}' or '{lst[1]}'"
		else:
			listed = ", ".join(f"'{e}'" for e in lst[0:-1])
			return f"{listed}, or '{lst[-1]}'"
	else:
		return f"'{lst}'"