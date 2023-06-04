from flask import  request
from Front import webapp
import os
import requests
from Front import serverdb_front
import base64
import json


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

    return json.dumps(response)


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

    # Send GET to MemCache
    r = requests.post('http://localhost:5001/get', data={'key': key})
    print("Http response: ", r)
    # Miss
    if r.status_code == 400:
        print("MISS !! Image not found in cache, will read from local storage.")
        abs_path = os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], img_name)
        with open(abs_path, "rb") as image:
            img_bytearray = base64.b64encode(image.read())

        response = requests.post("http://localhost:5001/put", data={'key': key, 'value': img_bytearray})
        print("Back response: ", response)
        print(img_bytearray)
        response = {
            "success": "true",
            "content": img_bytearray.decode('utf-8')
        }
        pass

    # Hit
    if r.status_code == 200:
        print("Hit !! Image found in cache.")
        response = {
            "success": "true",
            "content": r.json()
        }
    return response
