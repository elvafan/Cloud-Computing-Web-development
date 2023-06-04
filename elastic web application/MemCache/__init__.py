import boto3
import requests
from flask import Flask
import time
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from MemCache import serverdb_memcache
from MemCache.memcache import ServerMemCache

from botocore.exceptions import ClientError

from ManagerApp import managerStats

from Front import config



global cache
cache = ServerMemCache()
print("Cache initialized in backend: ", cache.memcache_dict)

def stat_updater():
    while True:
        db = serverdb_memcache.ServerDb()
        now = datetime.datetime.now()
        db.add_stat(now, cache.memcache_count, cache.usedsize, cache.total_get_request, cache.miss_count)
        managerStats.publish_cloudwatch_stats(1, "items_in_cache", cache.memcache_count)
        managerStats.publish_cloudwatch_stats(1, "total_size", cache.usedsize)
        managerStats.publish_cloudwatch_stats(1, "n_requests_served", cache.total_get_request)
        managerStats.publish_cloudwatch_stats(1, "n_requests_missed", cache.miss_count)
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



# new for a2
# TODO: CHANGE id

'''
global cache_pool
cache_pool = {
    "i-00ff00e5f0f095469": None, # Node 1
    "i-037460040dfdfc471": None,
    "i-0701e990e5856fc0d": None,
    "i-0cfdebf2e9439a9dc": None,
    "i-08b021881a42ddc5e": None,
    "i-0e0253ee10bbbebff": None,
    "i-049fad9a005c43bed": None,
    "i-0490a8f4d0378b0c8": None  # Node 8
}
'''
# global pool_option
# pool_option = "manual"



# # def conncect_ec2 ():
# #     ec2 = boto3.client('ec2', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
# #     # Do a dryrun first to verify permissions
# #     try:
# #         ec2.describe_instances(InstanceIds=[instance_id_default], DryRun=True)
# #     except ClientError as e:
# #         if 'DryRunOperation' not in str(e):
# #             raise

# #     # Dry run succeeded, run start_instances without dryrun
# #     try:
# #         response = ec2.describe_instances(InstanceIds=[instance_id_default], DryRun=False)
# #         print(response)
# #         #res = requests.get("http://000.000.000.000/latest/meta-data/instance-id")
# #         #instance_id = res.content.decode("utf-8")
# #         res = requests.get("http://000.000.000.000/latest/meta-data/public-ipv4")
# #         public_ipv4 = res.content.decode("utf-8")
# #         host_ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
# #         response = requests.post('http://' + str(host_ip_address) + ':5001/connect_from_ec2',
# #         json= {
# #             "ip_address":  public_ipv4,
# #             "instance_id": instance_id
# #         }
# #         )
# #         print(response)
# #         # TODO:  response contain info to init a memcache, according to the definition of ServerMemCache() need to save to db
# #         cache = ServerMemCache()
# #         print("Cache initialized in backend: ", cache.memcache_dict)
# #     except ClientError as e:
# #         print(e)

# def initilize_ec2_cache_node(instance_id):
#     ec2 = boto3.client('ec2', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
#     # Do a dryrun first to verify permissions
#     try:
#         ec2.describe_instances(InstanceIds=[instance_id], DryRun=True)
#     except ClientError as e:
#         if 'DryRunOperation' not in str(e):
#             raise

#      # Dry run succeeded, run start_instances without dryrun
#     try:
#         # TODO: Run backend
        
#         pass
#     except ClientError as e:
#         print(e)







