def find_illegal(collection, valid_type):
	"""
	'findillegals' is a helper method that returns the type of the first 
	item contained within a collection that does not match the specified 
	type.
	"""
	if isinstance(collection, dict):
			collection = collection.values()

	for item in collection:
		# because 'bool' is a subclass of 'int,' it won't fail if 'True' or 'False' is passed while 'int' is enforced
		if isinstance(item, bool):
			if isinstance(valid_type, tuple):
				if bool not in valid_type:
					return type(item)
			elif valid_type != bool:
				return type(item)
		elif not isinstance(item, valid_type):
			return type(item)
	return None
