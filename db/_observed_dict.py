from abc import ABC

class WatchedDict(dict, ABC):
	def __init__(self, val, db, key):
		super().__init__(val)
		self.db = db
		self.key = key

	def _persist(self):
		self.db[self.key] = dict(self)

	def values(self):
		return [self.__getitem__(key) for key in self]

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self._persist()

	def __getitem__(self, key):
		uncensored = super().__getitem__(key)
		if isinstance(uncensored, dict):
			return WatchedDict(uncensored, self, key)
		elif isinstance(uncensored, list):
			return WatchedList(uncensored, self, key)
		return uncensored
		
	def __delitem__(self, key):
		super().__delitem__(key)
		self._persist()

	def clear(self):
		super().clear()
		self._persist()

	def pop(self, key, default=Ellipsis):
		if default is Ellipsis:
			value = super().pop(key)
		else:
			value = super().pop(key, default)
		self._persist()
		return value

	def popitem(self):
		item = super().popitem()
		self._persist()
		return item

	def update(self, *args, **kwargs):
		super().update(*args, **kwargs)
		self._persist()

	def setdefault(self, key, default=None):
		if key in self:
			return super().__getitem__(key)
		super().__setitem__(key, default)
		self._persist()
		return default

	def unobserve(self):
		return dict(self)

	def __repr__(self) -> str:
		return "<WatchedDict "+str(dict(self))+">"
		
from ._observed_list import WatchedList
