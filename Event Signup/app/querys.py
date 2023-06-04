from __future__ import print_function  # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key
from flask import render_template, url_for, redirect, request
from datetime import datetime

from app import webapp
from app import config


TABLE_NAME = 'Events'


# TODO
# This query part should be able to deployed as lambda function 
# Modify following querys to report:
# 1. How many people in the event given event ID
# 2. Total Number of events created in the DB
# 3. Total number of evenrs Active in the DB
#
# You may want to change create_table schema 
# More querys can be added

@webapp.route('/event/query_createdata')
def event_query_createdate():

    # Check Table exists first
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')

    # try:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    conn = boto3.client('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)

    table = dynamodb.Table(TABLE_NAME)

    date = request.args.get('eventDate')
    # date = datetime.strptime(date, '%Y-%m-%d').strftime("%B %d, %Y")
    print("date: ", date)

    response = table.query(
        IndexName='EventDateIndex',
        KeyConditionExpression= Key('EventDate').eq(date)
    )

    records = {}
    images = {}

    for i in response['Items']:
        if i['EventTitle'] not in records:
            event_attrs = [i['EventDate'], i['EventDescription']]
            records[i['EventTitle']] = event_attrs
            EventId = i['EventId']
            s3_response_object = conn.get_object(Bucket=config.S3_BUCKET_NAME, Key=EventId)
            images[i['EventTitle']] = s3_response_object['Body'].read().decode('utf-8')

    print("records:", records)


    return render_template("event/signup_event.html", events=records, images=images)
    # except Exception as e:
    #     print(e)
    #     return str(e)
