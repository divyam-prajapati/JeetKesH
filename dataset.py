from collections import OrderedDict
import time
import asyncio

class ExpiringFIFOSet:
    def __init__(self, max_size=10, expiry_seconds=300):
        self.max_size = max_size
        self.expiry = expiry_seconds
        self._store = OrderedDict()  # {ca: (timestamp, data)}
        self._lock = asyncio.Lock()

    async def add(self, ca: str, data: dict = None) -> bool:
        async with self._lock:
            self._clean_expired()
            
            if ca in self._store:
                return False
                
            self._store[ca] = (time.time(), data)
            
            # Maintain FIFO size
            if len(self._store) > self.max_size:
                self._store.popitem(last=False)
                
            return True

    def _clean_expired(self):
        current_time = time.time()
        expired = [
            ca for ca, (ts, _) in self._store.items()
            if current_time - ts > self.expiry
        ]
        for ca in expired:
            del self._store[ca]

    async def contains(self, ca: str) -> bool:
        async with self._lock:
            self._clean_expired()
            return ca in self._store