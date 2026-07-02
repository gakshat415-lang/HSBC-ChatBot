import sys
import hashlib

class mock_xxhash:
    class xxh3_128:
        def __init__(self, data): self.data = data
        def digest(self): return hashlib.md5(self.data).digest()

sys.modules['xxhash'] = mock_xxhash
