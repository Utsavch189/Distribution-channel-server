from collections import OrderedDict

class Cache:

	def __init__(self, capacity=32):
		self.cache = OrderedDict()
		self.capacity = capacity

	def get(self, key):
		if key not in self.cache:
			return False
		else:
			self.cache.move_to_end(key)
			return self.cache[key]

	def put(self, key, value):
		self.cache[key] = value
		self.cache.move_to_end(key)
		if len(self.cache) > self.capacity:
			self.cache.popitem(last = False)
			
	def delete(self,key):
		self.cache.pop(key)

