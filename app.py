import os
from chalice import Chalice
import boto3
from botocore.exceptions import ClientError
import json

app = Chalice(app_name='s3-events')
app.debug = True

# Set the values in the .chalice/config.json file.
S3_BUCKET = os.environ.get('APP_BUCKET_NAME', 'qce2dp-access')
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'access')

@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'], suffix='.json')
def s3_handler(event):
    # get the event, pull the file from s3, read it, and insert into DDB
    pass

def get_s3_object(bucket, key):
    # get the object from s3
    pass

def insert_data_into_dynamodb(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    try:
        response = table.put_item(
            Item={
                'event_key': data['event_key'],
                'building_code': data['building_code'],
                'building_door_id': data['building_door_id'],
                'access_time': data['access_time'],
                'user_identity': data['user_identity']
            }
        )
        app.log.debug(f"DynamoDB response: {response}")
        return response
    except ClientError as e:
        app.log.error(f"Error inserting data into DynamoDB: {e}")
        raise e

@app.route('/access', methods=['GET'])
def get_access():
    # return all records from DDB
    pass