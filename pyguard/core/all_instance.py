def all_instance(collection, valid_type):
		"""
		'all_instance' is a helper method that checks if every item contained 
		within a collection are of a specified type.
		"""
		return all(isinstance(item, valid_type) for item in collection)