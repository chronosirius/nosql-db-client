import json
from abc import ABC
from os import listdir, remove, makedirs
from threading import Lock
from ._observed_dict import WatchedDict
from ._observed_list import WatchedList

class Database(ABC):
	def __init__(self, dir, proxy_function=None, default_wrapper=None):
		self.dir = dir
		try:
			makedirs(self.dir)
			print(f"[INFO] That directory ({self.dir}) didn't exist; it is created now.")
		except FileExistsError:
			pass
		self.lock = Lock()
		def _f(k): return Ellipsis
		def _c(v, **kwargs): return v
		self.proxy_fn = proxy_function or _f
		self.default_wrapper = default_wrapper or _c
		self.wrappers = {}

	def __setitem__(self, key, value):
		try:
			towrite = json.dumps(value.jsonify(), indent=4)
		except AttributeError:
			towrite = json.dumps(value, indent=4)

		self.lock.acquire()
		with open(f'{self.dir}/{key}', 'w+') as f:
			f.write(towrite)
		self.lock.release()

	def __getitem__(self, key, wrapper=None):
		if (prox_ret := self.proxy_fn(key)) != Ellipsis:
			return prox_ret
		if key in self.keys():
			self.lock.acquire()
			with open(f'{self.dir}/{key}', 'r') as f:
				val = json.loads(f.read())
			self.lock.release()
			if wrapper is None:
				if type(val) is list:
					return self.wrappers.get(list, self.default_wrapper)(WatchedList(val, self, key), trace={'db': self, 'key': key})
				elif type(val) is dict:
					return self.wrappers.get(dict, self.default_wrapper)(WatchedDict(val, self, key), trace={'db': self, 'key': key})
				else:
					return self.wrappers.get(type(val), self.default_wrapper)(val, trace={'db': self, 'key': key})
			else:
				if type(val) is list:
					return wrapper(WatchedList(val, self, key), trace={'db': self, 'key': key})
				elif type(val) is dict:
					return wrapper(WatchedDict(val, self, key), trace={'db': self, 'key': key})
				else:
					return wrapper(val, trace={'db': self, 'key': key})
		else:
			raise KeyError(key)

	def __delitem__(self, key):
		if key in self.keys():
			remove(f'{self.dir}/{key}')
		else:
			raise KeyError(key)

	def keys(self):
		return set(listdir(f'{self.dir}/'))

	def values(self):
		return [self[key] for key in self.keys()]
	
	def __repr__(self):
		return '<Database ('+self.dir+')>'
