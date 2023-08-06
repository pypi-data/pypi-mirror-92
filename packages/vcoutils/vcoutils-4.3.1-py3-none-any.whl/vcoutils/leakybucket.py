from time import time


class LeakyBucket:
    def __init__(self, timeout: int):
        self.timeout = timeout
        self.items = []

    def add(self) -> int:
        self.items.append((len(self.items), time()))
        return self.get()

    def get(self) -> int:
        items = []
        for item in self.items:
            if not item[1] + self.timeout < time():
                items.append(item)
        self.items = items
        return len(self.items)

    def __str__(self):
        return f"<LeakyBucket n={len(self.items)} t={self.timeout}>"

    def __repr__(self):
        return f"<LeakyBucket n={len(self.items)} t={self.timeout}>"


class LeakyBucketManager:
    def __init__(self, default_timeout: int = 60):
        self.timeout = default_timeout
        self.buckets = {}

    def add(self, name: str, timeout_override: int = None) -> int:
        if not name in self.buckets:
            self.buckets[name] = LeakyBucket(timeout_override if timeout_override else self.timeout)

        self.buckets[name].add()
        return self.buckets[name].get()

    def get(self, name: str) -> int:
        if not name in self.buckets:
            return 0

        return self.buckets[name].get()