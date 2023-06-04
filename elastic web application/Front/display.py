from flask import render_template, url_for, request
from Front import webapp
from flask import json
import os
import requests
import base64
import boto3

from Front import serverdb_front
from Front import config



@webapp.route('/display_page', methods=['GET'])
def display_page():
    return render_template("display.html")


@webapp.route('/display', methods=['POST'])
def display():

    key = request.form.get('key')
    print("DISPLAY: ", key)
    serverdb = serverdb_front.ServerDb()
    ret = serverdb.read_image(key)  # Here we read the name of the image stored in local file system
    print(ret)
    if ret != -1:
        img_name = ret
        response = webapp.response_class(
            response=json.dumps(img_name),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )
        return render_template("fail_on_display.html")

    # Send GET to MemCache - EC2
    # TODO: Route this to ec2 get, modify on ec2 side to get from proper instances
    ip_address_json = requests.get('http://localhost:5002/store', data={'key': key})
    
    ip_address =json.loads(ip_address_json.content.decode('utf-8'))
    print("Front: IP:", ip_address)
    # Update Stat
    requests.post('http://localhost:5001/updateStats_req')
    r = requests.post("http://"+str(ip_address)+":5001/get", data={'key': key})
    old_cache_size = requests.post("http://"+str(ip_address)+":5001/getUsedSize")
    old_cache_count = requests.post("http://"+str(ip_address)+":5001/getUsedCount")
    # Miss
    if r.status_code == 400:
        print("MISS !! Image not found in cache, will read from s3.")

        # Read From S
        conn = boto3.client('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
        s3_response_object = conn.get_object(Bucket=config.S3_BUCKET_NAME, Key=img_name)
        object_content = s3_response_object['Body'].read()

        # TODO: Route this to ec2 put, modify on ec2 side to store to proper instances
        response = requests.post("http://"+str(ip_address)+":5001/put", data={'key': key, 'value': object_content})
        print(response)
        # Update Stat
        requests.post('http://localhost:5001/updateStats_miss')
        # Update Stat
        new_cache_size = requests.post("http://"+str(ip_address)+":5001/getUsedSize")
        new_cache_count = requests.post("http://"+str(ip_address)+":5001/getUsedCount")
        diff_size = float(json.loads(new_cache_size.content.decode('utf-8'))) - float(json.loads(old_cache_size.content.decode('utf-8')))
        diff_count = float(json.loads(new_cache_count.content.decode('utf-8'))) - float(json.loads(old_cache_count.content.decode('utf-8')))
        print(json.loads(old_cache_size.content.decode('utf-8')))
        print(json.loads(old_cache_count.content.decode('utf-8')))
        print(json.loads(new_cache_size.content.decode('utf-8')))
        print(json.loads(new_cache_count.content.decode('utf-8')))
        print(diff_size)
        print(diff_count)
        requests.post('http://localhost:5001/updateStats_size', data={'size': str(diff_size)})
        requests.post('http://localhost:5001/updateStats_count', data={'count': str(diff_count)})
        return render_template("success_on_display_cache.html", image=object_content.decode('utf-8'))

    # TODO: Modify on ec2 side to get base64 from ec2 instance on success
    # Hit
    if r.status_code == 200:
        print("Hit !! Image found in cache.")
        # Update Stat
        requests.post('http://localhost:5001/updateStats_hit')
        return render_template("success_on_display_cache.html", image=r.json())

    return response