from flask import render_template
from ManagerApp import webapp
from Front import config

import boto3
import plotly.express as px
import pandas as pd
import os

import datetime


def publish_cloudwatch_stats(inst_id, metric_name, metric_value): 
    now = datetime.datetime.utcnow()
    cloudwatch_client = boto3.client('cloudwatch', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = cloudwatch_client.put_metric_data(
        Namespace = "MemCache_metrics",
        MetricData = [
            {
                'MetricName': metric_name,
                'Dimensions':[
                    {
                        'Name': 'Instance_ID',
                        'Value': str(inst_id)
                    }
                ],
                'Unit': 'Count',
                'Value': metric_value,
                'Timestamp': now,
                'StorageResolution': 1 # Hi-res
            }
        ]
    )
    print(metric_name, "stored with value: ",metric_value)
    return response

def get_cloudwatch_stats(inst_id, metric_name):
    cloudwatch_client = boto3.client('cloudwatch', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    now = datetime.datetime.utcnow()
    metrics_last_30_minutes = cloudwatch_client.get_metric_statistics(
        Namespace = "MemCache_metrics",
        MetricName = metric_name,
        Dimensions=[
            {
                'Name': 'Instance_ID', 
                'Value': str(inst_id)
            }
        ],
        StartTime = now - datetime.timedelta(seconds=30 * 60), # 30minutes
        EndTime = now,
        Period = 60,
        Statistics=['Maximum'],
        Unit = 'Count'
    )
    ret_data = []
    ret_time = []
    for datapoint in metrics_last_30_minutes['Datapoints']:
        ret_time.append(datapoint['Timestamp'])
        ret_data.append(datapoint['Maximum'])
    return ret_time, ret_data

@webapp.route('/manager_stats_page', methods=['GET'])
def manager_stats_page():

    # TODO: Implement this
    # Use charts to show the number of nodes as well as to aggregate statistics for the memcache pool including miss rate,
    # hit rate, number of items in cache, total size of items in cache, number of requests served per minute. 
    # The charts should display data for the last 30 minutes at 1-minute granularity.

    # TODO: Get metrics from Cloud Watch and read from it
    # TODO: Change inst_id here to each instance id 


    # Items in cache
    time_added, items_in_cache= get_cloudwatch_stats(inst_id=1, metric_name="items_in_cache")
    df = pd.DataFrame({'Time': time_added, 'Item number in cache': items_in_cache})
    fig = px.scatter(df, x='Time', y='Item number in cache', title="Item number in cache VS Time")
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "items_in_cache.html")
    fig.write_html(fig_path)

    # Total cache size
    time_added, total_size= get_cloudwatch_stats(inst_id=1, metric_name="total_size")
    df = pd.DataFrame({'Time': time_added, 'Occupied cache size': total_size})
    fig = px.scatter(df, x='Time', y='Occupied cache size', title="Occupied cache size VS Time")
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "total_size.html")
    fig.write_html(fig_path)

    # Number of requests served
    time_added, n_requests_served= get_cloudwatch_stats(inst_id=1, metric_name="n_requests_served")
    df = pd.DataFrame({'Time': time_added, 'Number of requests served': n_requests_served})
    fig = px.scatter(df, x='Time', y='Number of requests served', title="Number of requests served VS Time")
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "n_requests_served.html")
    fig.write_html(fig_path)

    # Hit rate and miss rate
    time_added, n_requests_missed= get_cloudwatch_stats(inst_id=1, metric_name="n_requests_missed")
    hit_rate = []
    miss_rate = []
    for i in range(len(n_requests_served)):
        if n_requests_served[i] == 0:
            hit_rate.append(0)
            miss_rate.append(0)
        else:
            miss_rate.append(n_requests_missed[i] / n_requests_served[i])
            hit_rate.append(1 - (n_requests_missed[i] / n_requests_served[i]))
    df = pd.DataFrame({'Time': time_added, 'Hit Rate': hit_rate})
    fig = px.scatter(df, x='Time', y='Hit Rate', title="Hit Rate VS Time")
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "hitrate.html")
    fig.write_html(fig_path)

    df = pd.DataFrame({'Time': time_added, 'Miss Rate': miss_rate})
    fig = px.scatter(df, x='Time', y='Miss Rate', title="Miss Rate VS Time")
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "missrate.html")
    fig.write_html(fig_path)

    return render_template("managerStats.html")