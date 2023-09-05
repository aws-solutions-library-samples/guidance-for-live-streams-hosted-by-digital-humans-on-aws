import boto3
import json
cors = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def lambda_handler(event, context):
    '''
      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    print("Received event: " + json.dumps(event, indent=2))

    #operation = event['operation']
    body_json  = json.loads(event['body'])
    operation = body_json['operation']

    if 'tableName' in body_json:
        dynamo = boto3.resource('dynamodb').Table(body_json['tableName'])

    operations = {
        'create': lambda x: dynamo.put_item(**x),
        'delete': lambda x: dynamo.delete_item(**x)
    }

    if operation in operations:
         
            operations[operation](body_json.get('payload'))
            return {
                'statusCode': 200,
                'body': json.dumps('success'),
                'headers':cor
            }
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))
    

    
    