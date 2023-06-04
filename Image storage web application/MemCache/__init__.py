from flask import Flask
import time
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from MemCache import serverdb_memcache
from MemCache.memcache import ServerMemCache





global cache
cache = ServerMemCache()
print("Cache initialized in backend: ", cache.memcache_dict)


def stat_updater():
    while True:
        db = serverdb_memcache.ServerDb()
        now = datetime.datetime.now()
        db.add_stat(now, len(cache.memcache_dict), cache.usedsize, cache.total_get_request, cache.miss_count)
        print("Stats updated at ", now)
        time.sleep(5)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=stat_updater, trigger="interval", seconds=5)
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

webapp = Flask(__name__)


from MemCache import memcache
from MemCache import main








