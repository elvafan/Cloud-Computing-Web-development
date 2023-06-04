from flask import Flask
import os

webapp = Flask(__name__)

from AutoScaler import autoScaler