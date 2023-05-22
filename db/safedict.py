from threading import Lock

class sdict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = Lock()

    def __setitem__(self, key, value):
        with self.lock:
            return super().__setitem__(key, value)

    def __getitem__(self, key):
        with self.lock:
            return super().__getitem__(key)

    def __delitem__(self, key):
        with self.lock:
            return super().__delitem__(key)
