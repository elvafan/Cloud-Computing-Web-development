from flask import Flask
import os

global memcache_dict

webapp = Flask(__name__)
memcache_dict = {}

from Front import main
from Front import upload
from Front import display
from Front import showkey
from Front import stats
from Front import configure
from Front import serverdb_front
from Front import testapi


IMG_FOLDER = os.path.join('static', 'images')
STATS_FOLDER = os.path.join('static', 'stats')
webapp.config['IMG_FOLDER'] = IMG_FOLDER
webapp.config['STATS_FOLDER'] = STATS_FOLDER




