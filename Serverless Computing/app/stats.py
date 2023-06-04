import datetime
import boto3
from app import config

def publish_cloudwatch_stats(inst_id, metric_name, metric_value): 
    now = datetime.datetime.utcnow()
    cloudwatch_client = boto3.client('cloudwatch', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
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
    cloudwatch_client = boto3.client('cloudwatch', region_name = 'us-east-1', aws_access_key_id = config.AWS_ACCESS_KEY_ID, aws_secret_access_key = config.AWS_SECRET_KEY)
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

        for i in response['Items']:
            records.append(i)
        print(len(response['Items']))
        publish_cloudwatch_stats(1, "entrys_in_db", len(response['Items']))