from abc import ABC

class WatchedDict(dict, ABC):
	def __init__(self, val, db, key):
		super().__init__(val)
		self.val = val
		self.db = db
		self.key = key

	def keys(self):
		return self.val.keys()

	def __setitem__(self, key, value):
		self.val[key] = value
		self.db[self.key] = self.val

	def __getitem__(self, key):
		if key in self.keys():
			if type(self.val.get(key)) == dict:
				return WatchedDict(self.val.get(key), self, key)
			elif type(self.get(key)) == list:
				return WatchedList(self.val.get(key), self, key)
			else:
				return self.val.get(key)
		else:
			raise KeyError(key)
		
	def __iter__(self):
		return iter(self.val.keys())

	def unobserve(self):
		return self.val

	def __repr__(self) -> str:
		return "<WatchedDict "+str(self.val)+">"
		
from .observed_list import WatchedList
