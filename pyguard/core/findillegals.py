def findillegals(collection, valid_type):
	if isinstance(collection, dict):
		collection = collection.values()		
	for item in collection:
		if not isinstance(item, valid_type):
			return type(item)
	return None
