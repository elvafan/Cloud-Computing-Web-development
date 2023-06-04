# TODO: Implement Auto Scaler here
import boto3
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
import math
import random
import datetime
import matplotlib.pyplot as plt

def scaler_updater():
    
    # Make sure all 8 Memcache is in running state
    #ec2_memcache.ec2_start()
    print("Booting, allow for 1 minute.....")

    


    miss_rate = 0.1
    pool_size = 8
    active_node_num = pool_size
    pool_list = []
    miss_rate_list = []
    start = datetime.datetime.now()
    for i in range(50):
        
        # TODO: Read current cache miss rate
        # If manual_mode, we do nothing
        miss_rate_list.append(miss_rate)
        pool_list.append(pool_size)
        old_pool_size = pool_size
        print(pool_size)
        print("AUTO MODE")
        max_miss_rate=0.8
        min_miss_rate=0.2
        expand_ratio=2
        shrink_ratio=0.5
        print(miss_rate)
        if miss_rate > max_miss_rate:
            active_node_num_h = active_node_num 
            active_node_num = min(math.ceil(active_node_num_h * expand_ratio), 8)
            pool_size = active_node_num

            miss_rate = 0.7 * miss_rate + random.uniform(-0.05, 0.05)

        elif miss_rate < min_miss_rate:
            active_node_num_h = active_node_num 
            active_node_num = max(math.ceil(active_node_num_h * shrink_ratio), 1)
            pool_size = active_node_num
            miss_rate = 1.2 * miss_rate + random.uniform(-0.05, 0.05)
        

        print("Miss Rate Should be read, now:", datetime.datetime.now())

        # Refresh Pool Status
        # time.sleep(1)
        # if (datetime.datetime.now() - start).total_seconds() > 20:
        #     break
        if old_pool_size == 8:
            miss_rate = miss_rate
            pass
        else:
            miss_rate = 1.1 * miss_rate
    plt.clf()

    plt.plot(pool_list,miss_rate_list)


    max_miss_rate=0.8
    min_miss_rate=0.2

    plt.axhline(y = max_miss_rate, color = 'b', linestyle = '-', label = "Max Miss Rate")
    plt.axhline(y = min_miss_rate, color = 'r', linestyle = '-', label = "Min Miss Rate")

    plt.legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')
    plt.title('Auto Scaler Shrinking Nodes')

    plt.xlabel("Pool Size")
    plt.ylabel("Miss Rate")
    plt.savefig("scaler.png")
    


# scheduler = BackgroundScheduler(daemon=True)
# scheduler.add_job(func=scaler_updater)
# #scheduler.add_job(func=scaler_updater, trigger="interval", seconds=10)
# scheduler.start()

scaler_updater()

