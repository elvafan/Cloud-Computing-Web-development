from flask import render_template
from ManagerApp import webapp, ec2_pool, ec2_memcache

@webapp.route('/manual_mode_page', methods=['GET', 'PUT'])
def manual_mode_page():
    current_pool_size = ec2_pool.nodes_numbers
    return render_template("manualMode.html", poolsize=current_pool_size)


@webapp.route('/manual_mode_increment', methods=['GET','POST', 'PUT'])
def manual_mode_increment():
    # TODO: Update pool size using these params
    if ec2_pool.nodes_numbers == 8:
        ec2_pool.pool_option = 'manual'
        current_pool_size = ec2_pool.nodes_numbers
    else:
        ec2_pool.pool_option = 'manual'
        success = 0
        for key, status in ec2_pool.cache_pool.items():
            if status == None:
                ec2_pool.cache_pool[key] = "Start"
                ec2_memcache.ec2_start()
                ec2_pool.increment()
                print("Manual Incre succeed: ", key)
                success = 1
                break
        if success == 0:
            print("Manual Incre Failed, Please try later")
        current_pool_size = ec2_pool.nodes_numbers
        

    return render_template("manualMode.html", poolsize=current_pool_size)


@webapp.route('/manual_mode_decrement', methods=['GET','POST', 'PUT'])
def manual_mode_decrement():
    BAD_STATES = ['stopping', 'starting', None, 'Start', 'Stop']
    # TODO: Update pool size using these params
    if ec2_pool.nodes_numbers == 1:
        ec2_pool.pool_option = 'manual'
        current_pool_size = ec2_pool.nodes_numbers
    else:
        ec2_pool.pool_option = 'manual'
        success = 0
        for key, status in ec2_pool.cache_pool.items():
            if status not in BAD_STATES:
                ec2_pool.cache_pool[key] = "Stop"
                ec2_memcache.ec2_stop()
                ec2_pool.decrement()
                print("Manual Decre succeed: ", key)
                success = 1
                break
        if success == 0:
            print("Manual decre Failed, Please try later")
        current_pool_size = ec2_pool.nodes_numbers
    
    return render_template("manualMode.html", poolsize=current_pool_size)
