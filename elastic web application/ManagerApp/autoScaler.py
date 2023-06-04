# TODO: Implement Auto Scaler here
import boto3
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
from ManagerApp import ec2_pool, ec2_memcache, autoMode, serverdb_manager, managerStats
import math

def scaler_updater():
    
    # Make sure all 8 Memcache is in running state
    ec2_memcache.ec2_start()
    print("Booting, allow for 1 minute.....")

    kl = list(ec2_pool.cache_pool.keys())
    pool_size = 8
    active_node_num = pool_size

    db = serverdb_manager.ServerDb()

    while True:
        
        # TODO: Read current cache miss rate
        print("Miss Rate Should be read, now:", datetime.datetime.now())
        time_added, n_requests_missed= managerStats.get_cloudwatch_stats(inst_id=1, metric_name="n_requests_missed")
        time_added, n_requests_served= managerStats.get_cloudwatch_stats(inst_id=1, metric_name="n_requests_served")
        if len(n_requests_served) == 0 or n_requests_served[-1] == 0:
            miss_rate = 0
        else:
            miss_rate = (n_requests_missed[-1] / n_requests_served[-1])
        print("Miss rate: ", miss_rate)

        
        # If manual_mode, we do nothing
        if ec2_pool.pool_option == 'manual':
            print("Manual MODE")
        else:
            print("AUTO MODE")
            as_config = db.read_as_config()
            max_miss_rate=as_config[0]
            min_miss_rate=as_config[1]
            expand_ratio=as_config[2]
            shrink_ratio=as_config[3]
            if miss_rate > max_miss_rate:
                active_node_num_h = active_node_num 
                active_node_num = min(math.ceil(active_node_num_h * expand_ratio), 8)
                for id in kl[:active_node_num]:
                    ec2_pool.cache_pool[id] = "Start"
                print(ec2_pool.cache_pool)
                ec2_memcache.ec2_start()
            elif miss_rate < min_miss_rate:
                active_node_num_h = active_node_num 
                active_node_num = max(math.ceil(active_node_num_h * shrink_ratio), 1)
                print(kl[active_node_num:active_node_num_h])
                for id in kl[active_node_num:active_node_num_h]:
                    ec2_pool.cache_pool[id] = "Stop"
                print(ec2_pool.cache_pool)
                ec2_memcache.ec2_stop()
        
        # Refresh Pool Status
        ec2_memcache.update_memcache_pool_status()
        time.sleep(60)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=scaler_updater)
#scheduler.add_job(func=scaler_updater, trigger="interval", seconds=10)
scheduler.start()