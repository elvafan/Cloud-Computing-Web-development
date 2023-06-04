from flask import render_template, url_for, request
from Front import webapp
from flask import json
from flask import logging
import os
import requests
import base64

from Front import serverdb_front
from Front import config

import boto3
from botocore.exceptions import ClientError
from moto import mock_s3



@webapp.route('/upload_page', methods=['GET'])
def upload_page():
    return render_template("upload.html")


@webapp.route('/upload', methods=['POST'])
def upload():

    key = request.form.get('key')

    # TODO (-Optional- Add more corner cases)
    # Error handling when file type is not correct
    if not key:
        response = webapp.response_class(
            response=json.dumps("Please specify a unique to upload a file."),
            status=400,
            mimetype='application/json'
        )
        return response

    
    new_img = request.files['image']
    img_name = key + "_" + new_img.filename  # Concatenate key at the front of the img name

    # Write file to local system
    # TODO: Remove this after s3 is implemented
    new_img.save(os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], img_name))



    print(("1 image:%s uploaded.", img_name))
    webapp.logger.debug("1 image:%s uploaded.", img_name)

    # Send INVALIDATE to Back
    r = requests.post("http://localhost:5001/invalidateKey", data={'key': key})
    print("HTTP response: ", r)

    # Make updates to RDBMS
    serverdb = serverdb_front.ServerDb()
    serverdb.insert_image(key, img_name)

    print("Success")

    with open(os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], img_name), "rb") as image:
            img_bytearray = base64.b64encode(image.read())

    # Write to S3 instance:
    content = upload_to_s3(img_bytearray, img_name)
    
    if content == img_bytearray:
        print("YES")
    #return render_template("success_on_display_cache.html", image=content.decode('utf-8'))
    return render_template('success_on_upload.html')

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
    conn = boto3.resource('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)

    try:
        object = conn.Object(config.S3_BUCKET_NAME, image_name)
        object.put(Body=image_data)
    except ClientError as e:
        print(e)
        return e