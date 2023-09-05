from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from contextlib import closing
import tempfile
cors = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    
    print(event, type(event))
    data=event['queryStringParameters']
    print(data)
    vr_module=data['vr_module']
    print(vr_module)

   
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('vr-demo')
    
    try:
        response = table.query(
        IndexName='vr-module-index',
        KeyConditionExpression=Key('vr_module').eq(vr_module),
        FilterExpression=Attr('playing').eq(True)
        )
        print(response)
        if 'Items' in response and len(response['Items']) == 1:
            response= response['Items'][0]
        elif 'Items' in response and len(response['Items']) == 0:
            response='noaction'
        
    except ClientError as e:
        print(e.response['Error']['Message'])
        response='noaction'
    else:
        print('Query response:', json.dumps(response, indent=4, cls=DecimalEncoder))
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(response, indent=4, cls=DecimalEncoder),
        'headers':cors
    }
