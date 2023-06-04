import hashlib
import boto3
import requests
from boto3 import ec2
from botocore.exceptions import ClientError
from flask import render_template, json,redirect, url_for, request

from ManagerApp import webapp
from ManagerApp import ec2_pool
from Front import config

BAD_STATES = ['stopping', 'starting', None, 'Start', 'Stop']

ec2 = boto3.client('ec2')
@webapp.route('/start_instance', methods=['GET', 'POST'])
# start an ec2 instances
def ec2_start():
    ec2 = boto3.client('ec2', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    id = None
    for key, status in ec2_pool.cache_pool.items():
        print(key, status)
        if status == "Start":
            id = key
        print("ID: ", id)
        if id != None:
            # Do a dryrun first to verify permissions
            try:
                ec2.start_instances(InstanceIds=[id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

            # Dry run succeeded, run start_instances without dryrun
            try:
                response = ec2.start_instances(InstanceIds=[id], DryRun=False)
                print(response)
            except ClientError as e:
                print(e)
            # TODO: Start Backend script

    response = webapp.response_class(
        response=json.dumps("ok"),
        status=200,
        mimetype='application/json'
    )
    return response

@webapp.route('/stop_instance', methods=['GET', 'POST'])
# start an ec2 instances
def ec2_stop():
    ec2 = boto3.client('ec2', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    id = None
    for key, status in reversed(ec2_pool.cache_pool.items()):
        if status == "Stop":
            id = key
        if id != None:
            # Do a dryrun first to verify permissions
            try:
                ec2.stop_instances(InstanceIds=[id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

            # Dry run succeeded, call stop_instances without dryrun
            try:
                response = ec2.stop_instances(InstanceIds=[id], DryRun=False)
                # print(response)
            except ClientError as e:
                print(e)
            # Stop Backend script (Probably no need)

    response = webapp.response_class(
        response=json.dumps("ok"),
        status=200,
        mimetype='application/json'
    )
    return response

@webapp.route('/store', methods=['GET'])
# similar to get
def ec2_store():
    ec2 = boto3.client('ec2', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    
    key = request.form.get('key')
    hash_key = hashlib.md5(key.encode()).hexdigest()
    hash_key = int(hash_key, base=16)
    list_active = []
    print(ec2_pool.cache_pool)
    for id, status in ec2_pool.cache_pool.items():
        print(status)
        if status not in BAD_STATES:
            list_active.append(id)
    print(hash_key)
    print(list_active)

    index = ((hash_key%16)+1)% len(list_active)
    # TODO: Route the key, image_content to the correspodning nodes'backend
    # FIXME: Change this index to instance IP
    print("IP: ", ec2_pool.cache_pool[list_active[index]])
    response = webapp.response_class(
        response=json.dumps(ec2_pool.cache_pool[list_active[index]]),
        status=200,
        mimetype='application/json'
    )
    return response

@webapp.route('/clear_cache_pool', methods = ['POST'])
def clear_cache_pool():
    """ Clear cache content
    """
    for id,status in ec2_pool.cache_pool.items():
        if status not in BAD_STATES:
            #clear active ports
            # Here status should be IP addr
            print(id, status)
            response = requests.post('http://' + str(status) + ':5001/clear')

    #return response


@webapp.route('/connect_from_ec2', methods=['POST'])
def connect_from_ec2():
    idip = request.get_json(force=True)
    ec2_pool.cache_pool[idip['instance_id']] = idip['ip_address']

# TODO: set and get
    massage = {
        'capacity' :  0,
        'replacement_policy': "LRU"
    }
    return massage

def broadcast_config():
    for id,status in ec2_pool.cache_pool.items():
        if status not in BAD_STATES:
            #clear active ports
            # Here status should be IP addr
            print(id, status)
            response = requests.post('http://' + str(status) + ':5001/refreshConfig')
    return response


def update_memcache_pool_status():
    ec2 = boto3.client('ec2', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    print("Check current the memcache pool status")

    # Dry run succeeded, run describe_instances without dryrun
    running_node_count = 0
    # try
    for inst_id in ec2_pool.cache_pool_list:
        print(inst_id," Status:")
        response = ec2.describe_instances(InstanceIds=[inst_id], DryRun=False)
        inst_state_name = response['Reservations'][0]['Instances'][0]['State']['Name']
        
        if (inst_state_name == 'running'):
            print("Running")
            ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            ec2_pool.cache_pool[inst_id] = ip_address
            running_node_count += 1
        elif (inst_state_name == 'pending'):
            ec2_pool.cache_pool[inst_id] = 'starting'
        elif (inst_state_name == 'stopping' or inst_state_name == 'shutting-down'):
            ec2_pool.cache_pool[inst_id] = 'stopping'
        else:
            ec2_pool.cache_pool[inst_id] = None

    print(ec2_pool.cache_pool)
    return running_node_count
    # except ClientError as e:
    #     print(e)





