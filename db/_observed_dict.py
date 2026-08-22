from abc import ABC

class WatchedDict(dict, ABC):
	def __init__(self, val, db, key):
		super().__init__(val)
		self.db = db
		self.key = key

	def _persist(self):
		self.db[self.key] = dict(self)

	def _wrap(self, key, value):
		if isinstance(value, dict):
			return WatchedDict(value, self, key)
		if isinstance(value, list):
			return WatchedList(value, self, key)
		return value

	def values(self):
		return [self.__getitem__(key) for key in self]

	def items(self):
		return [(key, self.__getitem__(key)) for key in self]

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self._persist()

	def __getitem__(self, key):
		return self._wrap(key, super().__getitem__(key))

	def get(self, key, default=None):
		if key in self:
			return self.__getitem__(key)
		return default
		
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

	def __ior__(self, other):
		result = super().__ior__(other)
		self._persist()
		return result

	def setdefault(self, key, default=None):
		if key in self:
			return self.__getitem__(key)
		super().__setitem__(key, default)
		self._persist()
		return default

	def unobserve(self):
		return dict(self)

	def __repr__(self) -> str:
		return "<WatchedDict "+str(dict(self))+">"
		
from ._observed_list import WatchedList
