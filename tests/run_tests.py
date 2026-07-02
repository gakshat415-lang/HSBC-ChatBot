import sys
import os
import hashlib

# Mock xxhash for Windows before pytest imports anything
class mock_xxhash:
    class xxh3_128:
        def __init__(self, data): self.data = data
        def digest(self): return hashlib.md5(self.data).digest()
sys.modules['xxhash'] = mock_xxhash

import pytest

if __name__ == "__main__":
    sys.exit(pytest.main(["tests/test_guardrails.py", "-v"]))
