from flask import render_template, request
from Front import webapp
from Front import serverdb_front
import requests

@webapp.route('/configure_page', methods=['GET'])
def configure_page():
    return render_template("configure.html")


@webapp.route('/update_config', methods=['POST'])
def update_config():
    capacity = request.form.get('cachesize')
    policy = request.form.get('policy')
    print(capacity, policy)

    # Cachesize not specified, remain old
    if not capacity:
        capacity = -1

    db = serverdb_front.ServerDb()

    db.update_configure(policy, capacity)

    return render_template("success_on_config.html")

@webapp.route('/clear_cache', methods=['POST'])
def clear_cache():

    # Send INVALIDATE to Back
    r = requests.post("http://localhost:5001/clear")
    print("HTTP response: ", r)

    return render_template("success_on_config.html")