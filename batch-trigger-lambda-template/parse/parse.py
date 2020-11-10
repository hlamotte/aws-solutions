#import boto3
from urllib.parse import unquote_plus

def process(bucket_name, file_key, batch=False):

    file_key = unquote_plus(file_key)

    # Do some processing after reading an object from s3

    #s3 = boto3.resource('s3')
    #obj = s3.Object(bucket_name, file_key)


    #file_data = obj.get()['Body'].read()
    #path = f's3://{bucket_name}/{file_key}'
    
    
