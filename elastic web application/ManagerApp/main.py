
from flask import render_template
from ManagerApp import webapp
from ManagerApp import managerStats

import time

@webapp.route('/')
def main():
    return render_template("main.html")
