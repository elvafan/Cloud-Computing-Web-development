from flask import render_template, url_for, request
from MemCache import webapp, cache
from flask import json



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
    cache.add(key, value)
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

@webapp.route('/refreshConfig', methods=['POST'])
def refreshConfiguration():
    cache.refresh_config()
    pass
    response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
        )
    return response

@webapp.route('/updateStats_miss', methods=['POST'])
def updateStats_miss():
    cache.miss_count += 1
    response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
    )
    return response

@webapp.route('/updateStats_hit', methods=['POST'])
def updateStats_hit():
    cache.hit_count += 1
    response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
    )
    return response

@webapp.route('/updateStats_req', methods=['POST'])
def updateStats_req():
    cache.total_get_request += 1
    response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
    )
    return response


@webapp.route('/updateStats_count', methods=['POST'])
def updateStats_count():
    count = request.form.get('count')
    cache.memcache_count += float(count)
    response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
    )
    return response


@webapp.route('/updateStats_size', methods=['POST'])
def updateStats_size():
    size = request.form.get('size')
    cache.usedsize += float(size)
    response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
    )
    return response



# FOllowing code will be on nodes

# @webapp.route('/getUsedSize', methods=['POST'])
# def refreshConfiguration():
#     response = webapp.response_class(
#         response=json.dumps(str(cache.usedsize)),
#         status=200,
#         mimetype='application/json'
#     )
#     return response

# @webapp.route('/getUsedCount', methods=['POST'])
# def refreshConfiguration():
#     response = webapp.response_class(
#         response=json.dumps(str(len(cache.memcache_dict))),
#         status=200,
#         mimetype='application/json'
#     )
#     return response
