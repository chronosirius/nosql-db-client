from abc import ABC

class WatchedList(list, ABC):
	def __init__(self, val, db, key):
		self.val = val
		self.db = db
		self.key = key

	def append(self, val):
		self.val.append(val)
		self.db[self.key] = self.val
		return self.val

	def remove(self, val):
		self.val.remove(val)
		self.db[self.key] = self.val
		return self
	
	def pop(self, index):
		e = self.val.pop(index)
		self.db[self.key] = self.val
		return e
	
	def __getitem__(self, slice_):
		#print('getitem called,', slice_)
		if type(slice_) == int:
			uncensored = self.val[slice_]
			if type(uncensored) == list:
				#print(WatchedList(uncensored, self, slice_))
				return WatchedList(uncensored, self, slice_)
			elif type(uncensored) == dict:
				#print(WatchedDict(uncensored, self, slice_))
				return WatchedDict(uncensored, self, slice_)
			else:
				return uncensored
		else:
			uncensored = self.val[slice_.start:slice_.stop:slice_.step]
			censored = uncensored.copy()
			for i, v in enumerate(uncensored):
				if type(v) == list:
					censored[i] = WatchedList(v, self, i)
				elif type(v) == dict:
					censored[i] = WatchedDict(v, self, i)
				else:
					censored[i] = v
			return censored

	def __setitem__(self, index, value):
		self.val[index] = value
		self.db[self.key] = self.val

	def __contains__(self, item):
		return item in self.val
	
	def __iter__(self):
		return iter(self.val)
		
	def __len__(self):
		return len(self.val)

	def unobserve(self):
		return self.val

	def index(self, item):
		return self.val.index(item)

	def __repr__(self) -> str:
		return '<WatchedList ' + str(self.val)+'>'
		
from ._observed_dict import WatchedDict
