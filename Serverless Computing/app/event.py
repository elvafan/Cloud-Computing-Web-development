from __future__ import print_function  # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key
from flask import render_template, url_for, redirect, request, json
import uuid
import hashlib
from datetime import time, date, datetime
from botocore.exceptions import ClientError
import base64
import os

from app import webapp
from app import config


TABLE_NAME = 'Events'

# Initialize DynamoDB Table - Events
@webapp.route('/event/create_table')
def event_create_table():
    
    # Check S3 Bucket Availability
    s3 = boto3.resource('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    bucket = s3.Bucket(config.S3_BUCKET_NAME)
    if bucket.creation_date:
        print("The bucket exists")
    else:
        print("The bucket does not exist")
        conn = boto3.client('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
        conn.create_bucket(Bucket=config.S3_BUCKET_NAME)
    
    # Check if exists:
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME in response['TableNames']:
        return render_template('event/table_already_exists.html')

    # Create Table if not exists
    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'EventId',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'EventTitle',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            GlobalSecondaryIndexes=[
                # TODO 
                # Add Secondary Index when needed
                {
                    'IndexName': "EventDateIndex",
                    'KeySchema': [
                        {
                            'AttributeName': 'EventDate',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'EventId',
                            'KeyType': 'RANGE'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['EventDescription', 'EventStatus', 'ParticipantList' ]
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "EventTitleIndex",
                    'KeySchema': [
                        {
                            'AttributeName': 'EventTitle',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'EventDate',
                            'KeyType': 'RANGE'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['EventDescription', 'EventStatus','ParticipantList']
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
            ],

            # Add required attributes
            # S - the attribute is of type String    N - the attribute is of type Number  B - the attribute is of type Binary
            AttributeDefinitions=[
                {
                    'AttributeName': 'EventId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'EventTitle',
                    'AttributeType': 'S'
                },
                # {
                #     'AttributeName': 'CreateDate',
                #     'AttributeType': 'S'
                # },
                {
                    'AttributeName': 'EventDate',
                    'AttributeType': 'S'
                },
                # {
                #     'AttributeName': 'EventStatus',
                #     'AttributeType': 'N'
                # },
                # {
                #     'AttributeName': 'EventDescription',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'ParticipantId',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'ParticipantName',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'ContactInfo',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'SignedUpDate',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'ParticipantRole',
                #     'AttributeType': 'S'
                # },
                


            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )    

        # Wait for table to be fully created
        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)

        return render_template('event/success_on_creating_table.html')

# Delete DynamoDB Table Events
@webapp.route('/event/delete_table')
def event_delete_table():
    
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    # Check if exists:
    response = client.list_tables()
    if TABLE_NAME in response['TableNames']:
        response = client.delete_table(
            TableName=TABLE_NAME
        )
        # Wait for table to be fully deleted
        waiter = client.get_waiter('table_not_exists')
        waiter.wait(TableName=TABLE_NAME)
        return render_template('event/success_on_deleting_table.html')
    else:
        return render_template('event/table_not_exist.html')


def event_putItem(eventId, eventTitle, description, eventDate, eventTime):
    # Check Table exists first
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')
    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
        table = dynamodb.Table(TABLE_NAME)

        today = date.today()
        createDate = today.strftime("%B %d, %Y")
        print(createDate)

        participantList = {}
        # Each entry contains:

        #'ParticipantId': participantId, 
        #'ParticipantName': participantName,
        #'ContactInfo': contactInfo,
        #'SignedUpDate': createDate,
        #'ParticipantRole': role,
        
        # TODO
        # (-Optional-)
        # Add attribute for event image key stored in S3 for extra feature
        
        response = table.put_item(
            Item={
                'EventId':eventId,
                'EventTitle': eventTitle,
                'CreateDate': createDate,
                'EventDate': eventDate,
                'EventTime': eventTime,
                'EventDescription': description,
                #'ParticipantId': participantId, 
                #'ParticipantName': participantName,
                #'ContactInfo': contactInfo,
                #'SignedUpDate': createDate,
                #'ParticipantRole': role,
                'ParticipantList' : participantList,
            }
        )

        return 

# TODO: 
# Create New Event Record with event host as first participant
@webapp.route('/event/load_new_event', methods=['GET', 'POST'])
def event_load_new_event():
    # Check Table exists first
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')

    # Load into table given 
    print("Loading data into table " + TABLE_NAME + "...")

    new_event_name = request.form.get('new_event_name')
    new_event_desc = request.form.get('new_event_desc')
    new_event_datetime = datetime.strptime(request.form.get('new_event_datetime'), "%Y-%m-%dT%H:%M")
    new_event_date = new_event_datetime.date().isoformat()
    new_event_time = new_event_datetime.time().isoformat()
    new_event_host = request.form.get('new_event_host')
    host_contact = request.form.get('host_contact')
    print("Date:", new_event_datetime)

    eventId = str(uuid.uuid4())
    print(eventId)

    # TODO:
    # Add a upload image and store the image to s3
    # Store the image name on s3 into our dynamodb
  
    new_img = request.files['image']
    new_img.save(os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], eventId))
    with open(os.path.join(webapp.root_path, webapp.config['IMG_FOLDER'], eventId), "rb") as image:
            img_bytearray = base64.b64encode(image.read())
    conn = boto3.resource('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    try:
        object = conn.Object(config.S3_BUCKET_NAME, eventId)
        object.put(Body=img_bytearray)
    except ClientError as e:
        print(e)
        return e

    event_putItem(
        eventId = eventId,
        eventTitle = new_event_name, 
        description = new_event_desc, 
        eventDate = new_event_date, 
        eventTime = new_event_time,
        # participantId = participantId, 
        # participantName = new_event_host, 
        # contactInfo = host_contact, 
        # role = role
        )

    # TODO:
    # Store this event id somewhere else

    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
        table = dynamodb.Table(TABLE_NAME)

        # response = table.query(
        #     IndexName='CreateDateIndex',
        #     KeyConditionExpression= Key('EventId').eq(eventId)
        # )

        # Scan here will display everything in the table
        response = table.scan()

        records = []

        for i in response['Items']:
            records.append(i)
        


        return render_template("event/success_on_creating_event.html", eventId=eventId)
    except Exception as e:
        return str(e)

# TODO:
# Probably modify this 
@webapp.route('/event/load_new_participant')
def event_load_new_participant():
    # Check Table exists first
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')

    # Load into table given 
    print("Loading data into table " + TABLE_NAME + "...")

    new_event_name = request.args.get('new_event_name')
    participantName = request.args.get('new_participant')
    contactInfo = request.args.get('new_contact_info')


    # Load event info
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    table = dynamodb.Table(TABLE_NAME)

    response = table.query(
        IndexName='EventTitleIndex',
        KeyConditionExpression= Key('EventTitle').eq(new_event_name)
    )

    print(response)
    if response is None:
        return render_template('event/event_not_exist.html')

    participantId = str(uuid.uuid4())
    ParticipantList = response['Items'][0]['ParticipantList']
    ParticipantList[participantId] = [participantName, contactInfo]
    print('ParticipantList:')
    print(ParticipantList)

    eventid = response['Items'][0]['EventId']

    response = table.update_item(
        Key={
            'EventId': eventid,
            'EventTitle': new_event_name,
        },
        UpdateExpression='SET ParticipantList = :val1',
        ExpressionAttributeValues={
            ':val1': ParticipantList
        }
    )

    # TODO: Render a page to print this to let user remember this ID
    return render_template('event/success_on_booking.html', receiptId = participantId)


@webapp.route('/event/list_all', methods=['POST'])
def event_list_all():
    # Check Table exists first

    password = request.form.get('password')
    if password != "admin":
        return render_template('event/login_failed.html')


    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    conn = boto3.client('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(IndexName="EventDateIndex")
    records = []
    images ={}

    for i in response['Items']:
        records.append(i)
        EventId = i['EventId']
        s3_response_object = conn.get_object(Bucket=config.S3_BUCKET_NAME, Key=EventId)
        images[i['EventTitle']] = s3_response_object['Body'].read().decode('utf-8')

    return render_template("event/events.html", events=records, images=images)


@webapp.route('/event/book_event')
def book_event_page():
    # Check Table exists first
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')


    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(IndexName='EventTitleIndex')
    records = {}

    # TODO:
    # Change what info is displayed here
    for i in response['Items']:
        if i['EventTitle'] not in records:
            event_attrs = [i['EventDate'], i['EventDescription']]
            records[i['EventTitle']] = event_attrs

    print("All: ", records)
    
    # TODO:
    # Modify this page to Add upload image function in html
    return render_template('event/book_event.html', events=records)

# TODO:
# Implement this 
@webapp.route('/event/signup_event')
def signup_event_page():
    # Check Table exists first
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')


    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
    conn = boto3.client('s3', region_name='us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)

    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(IndexName='EventTitleIndex')
    records = {}
    images = {}

    for i in response['Items']:
        if i['EventTitle'] not in records:
            event_attrs = [i['EventDate'], i['EventDescription']]
            records[i['EventTitle']] = event_attrs
            EventId = i['EventId']
            s3_response_object = conn.get_object(Bucket=config.S3_BUCKET_NAME, Key=EventId)
            images[i['EventTitle']] = s3_response_object['Body'].read().decode('utf-8')

    print("All: ", records)

    return render_template('event/signup_event.html', events=records, images=images)


# TODO:
# Implement me
@webapp.route('/event/cancel_event_page')
def cancel_event_page():
    return render_template('event/cancel_event.html')


@webapp.route('/event/event_cancel_confirm')
def cancel_event():
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')

    # Load into table given
    print("Loading data into table " + TABLE_NAME + "...")

    eventid = request.args.get('cancel_event_id')
    eventname = request.args.get('cancel_event_name')
    print(eventid)
    print(eventname)

    # Load event info
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=config.AWS_SECRET_KEY)
    table = dynamodb.Table(TABLE_NAME)

    table.delete_item(
        Key={
            'EventId': eventid,
            'EventTitle': eventname,
        }
    )
    return render_template('event/success_on_cancel_event.html')

# TODO:
# Implement me
@webapp.route('/event/cancel_participant_page')
def cancel_participant_page():
    return render_template('event/cancel_participate.html')

@webapp.route('/event/participant_cancel_confirm')
def cancel_participate():
    # Check Table exists first
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=config.AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return render_template('event/table_not_exist.html')

    # Load into table given
    print("Loading data into table " + TABLE_NAME + "...")

    event_name = request.args.get('cancel_event_name')
    participantid = request.args.get('cancel_participate_id')

    # Load event info
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=config.AWS_SECRET_KEY)
    table = dynamodb.Table(TABLE_NAME)

    response = table.query(
        IndexName='EventTitleIndex',
        KeyConditionExpression=Key('EventTitle').eq(event_name)
    )

    print(response)
    if response is None:
        return render_template('event/event_not_exist.html')

    ParticipantList = response['Items'][0]['ParticipantList']
    if participantid in ParticipantList:
        ParticipantList.pop(participantid)
    else:
        return render_template('event/participate_not_exist.html')

    eventid = response['Items'][0]['EventId']

    response = table.update_item(
        Key={
            'EventId': eventid,
            'EventTitle': event_name,
        },
        UpdateExpression='SET ParticipantList = :val1',
        ExpressionAttributeValues={
            ':val1': ParticipantList
        }
    )
    return render_template('event/success_on_cancel_participate.html')
