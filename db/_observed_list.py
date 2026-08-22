from abc import ABC

class WatchedList(list, ABC):
	def __init__(self, val, db, key):
		super().__init__(val)
		self.db = db
		self.key = key

	def _persist(self):
		self.db[self.key] = list(self)

	def _wrap(self, index, value):
		if isinstance(value, list):
			return WatchedList(value, self, index)
		if isinstance(value, dict):
			return WatchedDict(value, self, index)
		return value

	def append(self, val):
		super().append(val)
		self._persist()
		return self

	def remove(self, val):
		super().remove(val)
		self._persist()
		return self
	
	def pop(self, index=-1):
		e = super().pop(index)
		self._persist()
		return e

	def extend(self, otherlist):
		super().extend(otherlist)
		self._persist()
	
	def __getitem__(self, slice_):
		uncensored = super().__getitem__(slice_)
		if isinstance(slice_, int):
			return self._wrap(slice_, uncensored)
		else:
			censored = uncensored.copy()
			indices = range(*slice_.indices(len(self)))
			for i, index in enumerate(indices):
				censored[i] = self._wrap(index, uncensored[i])
			return censored

	def __iter__(self):
		for index in range(len(self)):
			yield self.__getitem__(index)

	def __reversed__(self):
		for index in range(len(self) - 1, -1, -1):
			yield self.__getitem__(index)

	def __setitem__(self, index, value):
		super().__setitem__(index, value)
		self._persist()

	def __delitem__(self, index):
		super().__delitem__(index)
		self._persist()

	def insert(self, index, value):
		super().insert(index, value)
		self._persist()

	def clear(self):
		super().clear()
		self._persist()

	def sort(self, *args, **kwargs):
		super().sort(*args, **kwargs)
		self._persist()

	def reverse(self):
		super().reverse()
		self._persist()

	def __iadd__(self, other):
		result = super().__iadd__(other)
		self._persist()
		return result

	def __imul__(self, value):
		result = super().__imul__(value)
		self._persist()
		return result

	def __contains__(self, item):
		return super().__contains__(item)

	def unobserve(self):
		return list(self)

	def index(self, item):
		return super().index(item)

	def __repr__(self) -> str:
		return '<WatchedList ' + str(list(self))+'>'
		
from ._observed_dict import WatchedDict
