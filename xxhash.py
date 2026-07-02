import hashlib

class xxh3_128:
    def __init__(self, data):
        self.data = data
    def digest(self):
        return hashlib.md5(self.data).digest()
