from flask import  request
from Front import webapp
import os
import requests
from Front import serverdb_front,config
import base64
import json
# TODO: Update this if necessary
import boto3
from botocore.exceptions import ClientError

@webapp.route('/api/upload', methods=['POST'])
def upload_for_test():

    key = request.form.get('key')

    if not key:
        response = {
            "success": "false",
            "error": {
                "code": 400,  # Bad Request
                "message": "Key empty, please specify some key"
            }
        }
        return json.dumps(response)

    # Write file to local system
    new_img = request.files['file']
    img_name = key + "_" + new_img.filename  # Concatenate key at the front of the img name
    new_img.save(os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], img_name))
    webapp.logger.debug("1 image:%s uploaded.", img_name)

    # Send INVALIDATE to Back
    r = requests.post("http://localhost:5001/invalidateKey", data={'key': key})
    if r.status_code == 200:
        response = {
            "success": "true"
        }
    else:
        response = {
            "success": "false",
            "error": {
                "code": 400,  # Bad Request
                "message": "Invalidate failed"
            }
        }
    # Make updates to RDBMS
    try:
        serverdb = serverdb_front.ServerDb()
    except:
        response = {
            "success": "false",
            "error": {
                "code": 400,  # Bad Request
                "message": "Database not accessible"
            }
        }
        return json.dumps(response)
    serverdb.insert_image(key, img_name)

    # A2 New Stuff
    with open(os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], img_name), "rb") as image:
        img_bytearray = base64.b64encode(image.read())

    # Write to S3 instance:
    content = upload_to_s3(img_bytearray, img_name)
    
    if content == img_bytearray:
        print("YES")
    #return render_template("success_on_display_cache.html", image=content.decode('utf-8'))

    return json.dumps(response)


def upload_to_s3(image_data, image_name):
    
    # Should not be here
    location = {'LocationConstraint': 'us-east-1'}
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(config.S3_BUCKET_NAME)
    if bucket.creation_date:
        print("The bucket exists")
    else:
        print("The bucket does not exist")
        conn = boto3.client('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=config.S3_BUCKET_NAME, CreateBucketConfiguration=location)
    


    #check bucket
    conn = boto3.resource('s3')

    try:
        object = conn.Object(config.S3_BUCKET_NAME, image_name)
        object.put(Body=image_data)
    except ClientError as e:
        print(e)
        return e


@webapp.route('/api/list_keys', methods=['POST'])
def list_keys_for_test():
    try:
        db = serverdb_front.ServerDb()
    except:
        response = {
            "success": "false",
            "error": {
                "code": 400,  # Bad Request
                "message": "Database not accessible"
            }
        }
        return json.dumps(response)
    ret = db.read_all_keys()

    response = {
        "success": "true",
        "keys": ret
    }
    return json.dumps(response)

@webapp.route('/api/key/<key_value>', methods=['POST'])
def retrieve_img_for_test(key_value):
    # TODO
    print("key: ", key_value)
    # Copy finished code here
    response = {
            "success": "false",
            "error": {
                "code": 400,
                "message": "Incorrect result"
            }
        }
    key = key_value
    try:
        serverdb = serverdb_front.ServerDb()
    except:
        response = {
            "success": "false",
            "error": {
                "code": 400,  # Bad Request
                "message": "Database not accessible"
            }
        }
        return json.dumps(response)
    ret = serverdb.read_image(key)  # Here we read the name of the image stored in local file system

    if ret != -1:
        img_name = ret
    else:
        response = {
            "success": "false",
            "error": {
                "code": 400,
                "message": "KEY NOT FOUND IN DB"
            }
        }
        return json.dumps(response)



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

        # Read From S3
        conn = boto3.client('s3')
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
        
        response = {
            "success": "true",
            "content": object_content.decode('utf-8')
        }

    # TODO: Modify on ec2 side to get base64 from ec2 instance on success
    # Hit
    if r.status_code == 200:
        print("Hit !! Image found in cache.")
        # Update Stat
        requests.post('http://localhost:5001/updateStats_hit')
        print("Hit !! Image found in cache.")
        response = {
            "success": "true",
            "content": r.json()
        }
    return response
