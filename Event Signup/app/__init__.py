from flask import Flask

webapp = Flask(__name__)

from app import main
from app import event
from app import querys
from app import stats

import os


IMG_FOLDER = os.path.join('static', 'images')
webapp.config['IMG_FOLDER'] = IMG_FOLDER

