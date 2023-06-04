from flask import render_template, request
from ManagerApp import webapp, ec2_pool
from ManagerApp import serverdb_manager

@webapp.route('/auto_mode_page', methods=['GET'])
def auto_mode_page():
    
    db = serverdb_manager.ServerDb()
    as_config = db.read_as_config()
    
    return render_template("autoMode.html", max_miss_rate=as_config[0], min_miss_rate=as_config[1], expand_ratio=as_config[2], shrink_ratio=as_config[3])

@webapp.route('/update_auto_mode_config', methods=['POST'])
def update_auto_mode_config():
    settings = {}
    settings["max_miss_rate_th"] = request.form.get('max_missrate_th')
    settings["min_miss_rate_th"] = request.form.get('min_missrate_th')
    settings["expand_ratio"] = request.form.get('expand_ratio')
    settings["shrink_ratio"] = request.form.get('shrink_ratio')

    db = serverdb_manager.ServerDb()

    for key, value in settings.items():
        db.update_configure_autoscaler(key, value)

    ec2_pool.pool_option = 'automatic'

    # TODO: Update auto-scaler using these params
    
    return render_template("success_on_config.html")

