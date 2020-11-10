import boto3
import json
from parse import parse


def lambda_handler(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    parse.process(bucket_name, file_key)

    message = f'File s3://{bucket_name}/{file_key} has been processed successfully'
    
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
