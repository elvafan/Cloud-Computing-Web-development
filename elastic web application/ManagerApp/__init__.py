from flask import Flask
import os
import boto3
from Front import config

webapp = Flask(__name__)
IMG_FOLDER = os.path.join('static', 'images')
STATS_FOLDER = os.path.join('static', 'stats')
webapp.config['IMG_FOLDER'] = IMG_FOLDER
webapp.config['STATS_FOLDER'] = STATS_FOLDER

class pool:
    nodes_numbers = None
    MAX_POOL_SIZE = 8
    MIN_POOL_SIZE = 1
    policy = "LRU"
    node_capacity = 1
    FORCE_START_ID = 'i-0195014b6d7ae58d0'


    # This will be the images on all possible nodes'cache, in LRU order
    active_keys_on_nodes =  {
        "i-00ff00e5f0f095469": [], # Node 1
        "i-037460040dfdfc471": [],
        "i-0701e990e5856fc0d": [],
        "i-0cfdebf2e9439a9dc": [],
        "i-08b021881a42ddc5e": [],
        "i-0e0253ee10bbbebff": [],
        "i-049fad9a005c43bed": [],
        "i-0490a8f4d0378b0c8": []  # Node 8
    }
    # cache_pool = {
    #     "i-00ff00e5f0f095469": None, # Node 1
    #     "i-037460040dfdfc471": None,
    #     "i-0701e990e5856fc0d": None,
    #     "i-0cfdebf2e9439a9dc": None,
    #     "i-08b021881a42ddc5e": None,
    #     "i-0e0253ee10bbbebff": None,
    #     "i-049fad9a005c43bed": None,
    #     "i-0490a8f4d0378b0c8": None  # Node 8
    # }
    cache_pool = {
        "i-0195014b6d7ae58d0": 'Start', # We always want to have one to start
        "i-06d4aee6b03cfbd29": None,
        "i-06550ba0897ecab24": None,
        "i-0142c7cd461c02034": None,
        "i-06a74e65817c501c4": None,
        "i-0d583786d2f5aada4": None,
        "i-0e4cfc09e67b28cbf": None,
        "i-056bab31745fe9379": None
    }
    cache_pool_list = [
        "i-0195014b6d7ae58d0",
        "i-06d4aee6b03cfbd29",
        "i-06550ba0897ecab24",
        "i-0142c7cd461c02034",
        "i-06a74e65817c501c4",
        "i-0d583786d2f5aada4",
        "i-0e4cfc09e67b28cbf",
        "i-056bab31745fe9379"
    ]
    # manual or automatic
    pool_option = "manual"

    def __init__(self):
        self.nodes_numbers = 0
        for inst_id in self.cache_pool_list:
            ec2 = boto3.client('ec2', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
            print(inst_id," Status:")
            response = ec2.describe_instances(InstanceIds=[inst_id], DryRun=False)
            inst_state_name = response['Reservations'][0]['Instances'][0]['State']['Name']
            if (inst_state_name == 'running'):
                print("Running")
                ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
                self.cache_pool[inst_id] = ip_address
                self.nodes_numbers += 1
            elif (inst_state_name == 'pending'):
                self.cache_pool[inst_id] = 'starting'
                print("Starting")
            elif (inst_state_name == 'stopping' or inst_state_name == 'shutting-down'):
                self.cache_pool[inst_id] = 'stopping'
                print("Stopping")
            else:
                self.cache_pool[inst_id] = None
                print("IDLE")
        print(self.nodes_numbers)
    
    def increment(self):
        self.nodes_numbers = min(self.nodes_numbers + 1, self.MAX_POOL_SIZE)
    
    def decrement(self):
        self.nodes_numbers = max(self.nodes_numbers - 1, self.MIN_POOL_SIZE)


global ec2_pool
ec2_pool = pool()


# New conponents for A2
from ManagerApp import main
from ManagerApp import managerApp
from ManagerApp import managerStats
from ManagerApp import manualMode
from ManagerApp import autoMode

from ManagerApp import autoScaler






