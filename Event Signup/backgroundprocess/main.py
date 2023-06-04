import json
import datetime, time
#from apscheduler.schedulers.background import BackgroundScheduler
import boto3

AWS_ACCESS_KEY_ID = 'AKIATKAFAAMC4Q3Q7NXJ'
AWS_SECRET_KEY = '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'
TABLE_NAME = 'Events'

#scheduler = BackgroundScheduler(daemon=True)

# BOTO3 aws ARN layer:
# arn:aws:lambda:us-east-1:113088814899:layer:Klayers-python37-boto3:3
sample_response = {
    'Items': 
        [{'EventTitle': "aaa", 'EventDescription': '12312312', 'EventId': '47bce5c74f589f4867dbd57e9ca9f808', 'EventDate': '2022-12-02', 'ParticipantId': 'ab86a1e1ef70dff97959067b723c5c24','ParticipantList':[]}, 
{'EventTitle': "bbb",'EventDescription': '113331', 'EventId': 'fdfcdebadad8143f39f75a024b689857', 'EventDate': '2022-12-02', 'ParticipantId': '7815696ecbf1c96e6894b779456d330e', 'ParticipantList':[]}, 
{'EventTitle': "ccc",'EventDescription': '13213123', 'EventId': '274da997412973c08cf7e78724153f55', 'EventDate': '2023-01-08', 'ParticipantId': 'b6d767d2f8ed5d21a44b0e5886680cb9','ParticipantList':[] },
 {'EventTitle': "ddd",'EventDescription': '213123', 'EventId': 'e368b9938746fa090d6afd3628355133', 'EventDate': '2022-12-07', 'ParticipantId': 'b6d767d2f8ed5d21a44b0e5886680cb9','ParticipantList': []}],
 'Count': 4, 'ScannedCount': 4, 'ResponseMetadata': {'RequestId': 'DR7UHE7OKM0351EOC23KPAJF4BVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 
 'HTTPHeaders': {'server': 'Server', 
 'date': 'Fri, 16 Dec 2022 03:58:08 GMT', 
 'content-type': 'application/x-amz-json-1.0',
  'content-length': '738', 'connection': 'keep-alive', 
  'x-amzn-requestid': 'DR7UHE7OKM0351EOC23KPAJF4BVV4KQNSO5AEMVJF66Q9ASUAAJG',
   'x-amz-crc32': '1274167783'}, 'RetryAttempts': 0}
   }

def publish_cloudwatch_stats(inst_id, metric_name, metric_value): 
    now = datetime.datetime.utcnow()
    cloudwatch_client = boto3.client('cloudwatch', region_name = 'us-east-1', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_KEY)
    response = cloudwatch_client.put_metric_data(
        Namespace = "A3_metrics",
        MetricData = [
            {
                'MetricName': metric_name,
                'Dimensions':[
                    {
                        'Name': 'Instance_ID',
                        'Value': str(inst_id)
                    }
                ],
                'Unit': 'Count',
                'Value': metric_value,
                'Timestamp': now,
                'StorageResolution': 1 # Hi-res
            }
        ]
    )
    print(metric_name, "stored with value: ",metric_value)
    return response

def get_cloudwatch_stats(inst_id, metric_name):
    cloudwatch_client = boto3.client('cloudwatch', region_name = 'us-east-1', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_KEY)
    now = datetime.datetime.utcnow()
    metrics_last_30_minutes = cloudwatch_client.get_metric_statistics(
        Namespace = "A3_metrics",
        MetricName = metric_name,
        Dimensions=[
            {
                'Name': 'Instance_ID', 
                'Value': str(inst_id)
            }
        ],
        StartTime = now - datetime.timedelta(seconds=30 * 60), # 30minutes
        EndTime = now,
        Period = 60,
        Statistics=['Maximum'],
        Unit = 'Count'
    )
    ret_data = []
    ret_time = []
    for datapoint in metrics_last_30_minutes['Datapoints']:
        ret_time.append(datapoint['Timestamp'])
        ret_data.append(datapoint['Maximum'])
    return ret_time, ret_data
    
def stat_updater():
    # TODO: 
    # Implement this function
    TABLE_NAME = 'Events'
    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        publish_cloudwatch_stats(1, "entrys_in_db", 0)

    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_KEY)
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan(IndexName='EventDateIndex')
        records = []
        total_num_participants = 0
        for i in response['Items']:
            records.append(i)
            total_num_participants += len(i['ParticipantList'])
        print(len(response['Items']))
        publish_cloudwatch_stats(1, "entrys_in_db", len(response['Items']))
        publish_cloudwatch_stats(1, "total_participants_in_db", total_num_participants)



def lambda_handler(event, context):
    # TODO implement
    stat_updater()

    client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_KEY)
    response = client.list_tables()
    if TABLE_NAME not in response['TableNames']:
        return {
            'statusCode': 400,
            'body': json.dumps("Table not found")
        }

    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_KEY)
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan(IndexName='EventDateIndex')
        #response = sample_response
        html_content = "<html><head><h1>Available Events Summary</h1></head>"

        # TODO:
        # Parse response to display how many events and how many participants are there for each event.
        html_content += "<body>"
        for i in response['Items']:
            html_content += "<table>"
            html_content = html_content + "Title: " + i['EventTitle']
    
            html_content += "<tr>"
            html_content = html_content + "<td>" + "Event Description:" + "</td>"
            html_content = html_content + "<td>" + i['EventDescription'] + "</td>"
            html_content += "</tr>"

            html_content += "<tr>"
            html_content = html_content + "<td>" + "Event Date:" + "</td>"
            html_content = html_content + "<td>" + i['EventDate'] + "</td>"
            html_content += "</tr>"

            html_content += "<tr>"
            html_content = html_content + "<td>" + "Number of participants:" + "</td>"
            html_content = html_content + "<td>" + str(len(i['ParticipantList'])) + "</td>"
            html_content += "</tr>"

            html_content += "</table><br><br>"

        html_content += "</body></html>"
        
        print(html_content)

        return {
            'statusCode': 200,
            'body': html_content,
             # 'body': json.dumps(str(len(response['Items']))),
            'headers': {
                'Content-Type': 'text/html',
            }
        }
   

        

def main():
    #scheduler.add_job(func=stat_updater, trigger="interval", seconds=5)
    #scheduler.start()
    # while True:
    #     now = datetime.datetime.now()
    #     #stat_updater()
    #     print("Stats updated at ", now )
    #     time.sleep(5)
    #return render_template("event/main.html")
    lambda_handler("","")


if __name__ == "__main__":
    main()