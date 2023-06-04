from flask import render_template
from Front import webapp
from Front import serverdb_front

import plotly.express as px
import pandas as pd
import os

@webapp.route('/stats_page', methods=['GET'])
def stats_page():

    db = serverdb_front.ServerDb()
    time_added, items_in_cache, total_size, n_requests_served, n_requests_missed = db.read_past_10min_stats()

    # Items in cache
    df = pd.DataFrame({'Time': time_added, 'Item number in cache': items_in_cache})
    fig = px.line(df, x='Time', y='Item number in cache', title="Item number in cache VS Time", markers=True)
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "items_in_cache.html")
    fig.write_html(fig_path)

    # Total cache size
    df = pd.DataFrame({'Time': time_added, 'Occupied cache size': total_size})
    fig = px.line(df, x='Time', y='Occupied cache size', title="Occupied cache size VS Time", markers=True)
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "total_size.html")
    fig.write_html(fig_path)

    # Number of requests served
    df = pd.DataFrame({'Time': time_added, 'Number of requests served': n_requests_served})
    fig = px.line(df, x='Time', y='Number of requests served', title="Number of requests served VS Time", markers=True)
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "n_requests_served.html")
    fig.write_html(fig_path)

    # Hit rate and miss rate
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
    fig = px.line(df, x='Time', y='Hit Rate', title="Hit Rate VS Time", markers=True)
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "hitrate.html")
    fig.write_html(fig_path)

    df = pd.DataFrame({'Time': time_added, 'Miss Rate': miss_rate})
    fig = px.line(df, x='Time', y='Miss Rate', title="Miss Rate VS Time", markers=True)
    fig_path = os.path.join(webapp.root_path, webapp.config['STATS_FOLDER'], "missrate.html")
    fig.write_html(fig_path)
    return render_template("statistics.html")