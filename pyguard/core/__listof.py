from collections import UserList

class ListOf(UserList):
	def __init__(self, *data):
		UserList.__init__(self, list(data))

	def append(self, item):
		self.__validate_item(item, "append()")
		if item in self.data:
			raise(TypeError(f"{item.__name__} already in list"))
		else:
			self.data.append(item)

	def insert(self, i, item):
		self.__validate_item(item, "insert()")
		if item in self.data:
			raise(TypeError(f"{item.__name__} already in list"))
		else:
			self.data.insert(i, item)

	def extend(self, other):
		
		unique = [i for i in other if i not in self.data]
		self.data.extend(unique)

	def __validate_item(self, item, method):
		if not isinstance(item, type):
			raise(TypeError(f'{method} expects item of type "type"'))




l = ListOf(str, int)
l.extend([int, 's'])

print(l)





