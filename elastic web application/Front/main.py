
from flask import render_template
from Front import webapp


@webapp.route('/')
def main():
    return render_template("main.html")
