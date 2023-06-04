from flask import render_template, url_for, request
from MemCache import webapp, cache
from flask import json
from flask import logging


@webapp.route('/')
def main():
    return render_template("main.html")


@webapp.route('/get', methods=['POST'])
def get():
    key = request.form.get('key')
    print("Back: ", key)

    result = cache.get(key)

    if result == -1:
        # Miss
        response = webapp.response_class(
            response=json.dumps("MISS"),
            status=400,
            mimetype='application/json'
        )
    else:
        # Hit
        value = cache.memcache_dict[key]
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    return response


@webapp.route('/put', methods=['POST'])
def put():

    key = request.form.get('key')
    value = request.form.get('value')

    # if key is not in the dict, create a new one, if existed, update with new value. check?
    cache.add(key, value);
    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response


@webapp.route('/clear', methods=['POST'])
def clear():
    cache.clear()
    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response


@webapp.route('/invalidateKey', methods=['POST'])
def invalidateKey():
    key = request.form.get('key')
    cache.remove(key)
    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response


def refreshConfiguration():
    pass
