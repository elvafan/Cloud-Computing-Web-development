
from flask import render_template, url_for, redirect
from app import webapp

import datetime


@webapp.route('/')
def main():
    return render_template("event/main.html")


@webapp.route('/event')
def event():
    return render_template("event/main.html")

