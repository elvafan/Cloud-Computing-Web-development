from flask import render_template, url_for, request
from Front import webapp
from flask import json
import os
import requests
import base64

from Front import serverdb_front


@webapp.route('/display_page', methods=['GET'])
def display_page():
    return render_template("display.html")


@webapp.route('/display', methods=['POST'])
def display():

    key = request.form.get('key')
    print("DISPLAY: ", key)
    serverdb = serverdb_front.ServerDb()
    ret = serverdb.read_image(key)  # Here we read the name of the image stored in local file system

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

    # Send GET to MemCache
    r = requests.post('http://localhost:5001/get', data={'key': key})
    print("Http response: ", r)
    # Miss
    if r.status_code == 400:
        print("MISS !! Image not found in cache, will read from local storage.")
        local_img = os.path.join(webapp.config['IMG_FOLDER'], img_name)

        abs_path = os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], img_name)
        with open(abs_path, "rb") as image:
            img_bytearray = base64.b64encode(image.read())

        response = requests.post("http://localhost:5001/put", data={'key': key, 'value': img_bytearray})
        print(response)
        # TODO
        # Send PUT to MemCache if it's not stored before
        return render_template("success_on_display.html", user_image=local_img)

        pass

    # Hit
    if r.status_code == 200:
        print("Hit !! Image found in cache.")
        return render_template("success_on_display_cache.html", image=r.json())
        pass
    return response