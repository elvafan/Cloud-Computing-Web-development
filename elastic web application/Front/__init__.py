from flask import Flask
import os
import boto3
from botocore.client import ClientError

global memcache_dict

memcache_dict = {}

webapp = Flask(__name__)
from Front import main
from Front import upload
from Front import display
from Front import showkey
from Front import stats
from Front import configure
from Front import serverdb_front
from Front import test_api

# New conponents for A2
from Front import config


# For Testing only, please remove when using real s3

IMG_FOLDER = os.path.join('static', 'images')
STATS_FOLDER = os.path.join('static', 'stats')
webapp.config['IMG_FOLDER'] = IMG_FOLDER
webapp.config['STATS_FOLDER'] = STATS_FOLDER


# Add aws
# Update the path below.
# file = 'C:/Users/Fuen/.aws/credentials'

# # Update keys below.
# AWS_ACCESS_KEY_ID = 'AKIATKAFAAMC4Q3Q7NXJ'
# AWS_SECRET_KEY = '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'

# with open(file, 'w') as filetowrite:
#     myCredential = f"""[default]
# aws_access_key_id={config.AWS_ACCESS_KEY_ID}
# aws_secret_access_key={config.AWS_SECRET_KEY}
# """
#     filetowrite.write(myCredential)

# # Update the path below.
# file = 'C:/Users/Fuen/.aws/config'

# with open(file, 'w') as filetowrite:
#     myCredential = """[default]
#                       region = us-east-1
#                       output = json
#                       [profile prod]
#                       region = us-east-1
#                       output = json"""
#     filetowrite.write(myCredential)




