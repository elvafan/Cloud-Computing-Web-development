from flask import render_template, url_for, request
from Front import webapp
from flask import json
from flask import logging
import os
import requests

from Front import serverdb_front


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

    # Write file to local system
    new_img = request.files['image']
    img_name = key + "_" + new_img.filename  # Concatenate key at the front of the img name
    new_img.save(os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], img_name))

    print(("1 image:%s uploaded.", img_name))
    webapp.logger.debug("1 image:%s uploaded.", img_name)

    # Send INVALIDATE to Back
    r = requests.post("http://localhost:5001/invalidateKey", data={'key': key})
    print("HTTP response: ", r)

    # Make updates to RDBMS
    serverdb = serverdb_front.ServerDb()
    serverdb.insert_image(key, img_name)

    return render_template('success_on_upload.html')