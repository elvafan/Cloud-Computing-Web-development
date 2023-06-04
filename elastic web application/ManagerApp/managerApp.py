from flask import render_template, request
import boto3

from ManagerApp import webapp, ec2_pool
from ManagerApp import serverdb_manager
from Front import config
from ManagerApp import ec2_memcache


@webapp.route('/manager_page', methods=['GET'])
def manager_page():
    return render_template("managerApp.html")


@webapp.route('/update_manager_config', methods=['POST'])
def update_manager_config():
    capacity = request.form.get('cachesize')
    policy = request.form.get('policy')
    print(capacity, policy)

    # Cachesize not specified, remain old
    if not capacity:
        capacity = -1

    db = serverdb_manager.ServerDb()
    db.update_a1_config(policy, capacity)

    # TODO: Broadcast change to all nodes
    return render_template("success_on_config.html")

@webapp.route('/clear_memcache_allnodes', methods=['POST'])
def clear_memcache_allnodes():

    # TODO: Implement this 
    # Clearing memcache data: A button to clear the content of all memcache nodes in the pool.
    ec2_memcache.clear_cache_pool()

    return render_template("success_on_config.html")

@webapp.route('/delete_all_data', methods=['POST'])
def delete_all_data():

    # Deleting all application data: A button to delete image data stored in RDS as well as all image files stored in S3, and clear the content of all memcache nodes in the pool
    
    #Clear S3 Bucket
    conn = boto3.resource('s3')
    bucket = conn.Bucket(config.S3_BUCKET_NAME)
    bucket.objects.all().delete()
    
    
    
    db = serverdb_manager.ServerDb()
    db.clear_all_image_data()
    # TODO: Sync changes to RDS
    # TODO: Call clear_memcache_allnodes
    ec2_memcache.clear_cache_pool()
    return render_template("success_on_config.html")