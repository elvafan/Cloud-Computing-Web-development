# all method for memcache
import random
from MemCache import serverdb_memcache

DEFAULT_CACHE_SIZE = 16
MB_TO_BYTES = 1048576


class ServerMemCache:
    def __init__(self):
        db = serverdb_memcache.ServerDb()
        policy, capacity = db.read_config()
        self.capacity = capacity * MB_TO_BYTES
        self.policy = policy

        self.usedsize = 0
        self.total_get_request = 0
        self.hit_count = 0
        self.miss_count = 0
        self.memcache_dict = {}
        # keep track the key of item, sorted from least recent usea to most recent used.
        self.memcache_recentused = []

    def get(self, key):
        self.total_get_request += 1
        if key in self.memcache_dict:
            # cache hit
            value = self.memcache_dict[key];
            # move the key to most recent used
            self.memcache_recentused.remove(key)
            self.memcache_recentused.append(key)
            # increase hit count
            self.hit_count += 1
            return value
        else:
            # cache miss
            self.miss_count += 1
            return -1

    def add(self, key, value):
        self.refresh_config()
        img_size = (len(value) * 3) / 4  # need to change

        # Clear cache if it can't fit current img
        if self.capacity < img_size:
            self.memcache_dict.clear()
            self.memcache_recentused.clear()
            self.usedsize = 0
        else:
            # check space
            while self.capacity - self.usedsize < img_size:
                if self.policy == "LRU":
                    remove_pos = 0
                else:
                    remove_pos = random.randint(0, len(self.memcache_recentused))
                removed_key = self.memcache_recentused.pop(remove_pos)
                removed_value = self.memcache_dict.pop(removed_key)
                self.usedsize -= (len(removed_value) * 3) / 4
            self.memcache_dict[key] = value
            self.memcache_recentused.append(key)
            self.usedsize += img_size

    def clear(self):
        self.memcache_dict.clear()
        self.memcache_recentused.clear()
        self.usedsize = 0
        self.total_get_request = 0
        self.hit_count = 0
        self.miss_count = 0

    def remove(self, key):
        if key in self.memcache_dict:
            self.memcache_recentused.remove(key)
            removed_value = self.memcache_dict.pop(key)
            self.usedsize -= (len(removed_value) * 3) / 4

    def refresh_config(self):
        db = serverdb_memcache.ServerDb()
        policy, capacity = db.read_config()
        self.capacity = capacity * MB_TO_BYTES
        self.policy = policy
        pass


