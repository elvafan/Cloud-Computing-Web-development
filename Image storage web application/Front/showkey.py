from flask import render_template
from Front import webapp

from Front import serverdb_front


@webapp.route('/keys_page', methods=['GET'])
def keys_page():
    dbms_implemented = True
    current_keys = []
    if dbms_implemented:
        # Read current keys from dbms and load them into current_keys
        db = serverdb_front.ServerDb()
        current_keys = db.read_all_keys()
        pass

    return render_template("available_keys.html", keys=current_keys)


