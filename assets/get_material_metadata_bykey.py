
import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import *

cors = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        #  if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        #  otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    
    print(event, type(event))
    data = json.loads(event.get('body'))
    user_id=data.get('user_id','')
    print(data, type(data))
    # user_id='VR-demo'

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('vr-demo')
    response = table.query(
         KeyConditionExpression = Key('demo_name').eq(user_id)
    )
    s=str(response)
    json_object = json.dumps(response,cls=DecimalEncoder)
    
    
    
    return {
        'statusCode': 200,
        'headers': cors,
        'body': json_object
    }
