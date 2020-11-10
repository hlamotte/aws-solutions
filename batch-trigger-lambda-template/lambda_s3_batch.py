from botocore.exceptions import ClientError

from parse import parse


def lambda_handler(event, context):

    # Prepare results
    results = []
    
    # Parse job parameters from S3 Batch Operations
    jobId = event['job']['id']
    invocationId = event['invocationId']
    invocationSchemaVersion = event['invocationSchemaVersion']
    
    # Parse Amazon S3 Key, Key Version, and Bucket ARN
    taskId = event['tasks'][0]['taskId']
    file_key = event['tasks'][0]['s3Key']
    s3VersionId = event['tasks'][0]['s3VersionId']
    s3BucketArn = event['tasks'][0]['s3BucketArn']
    bucket_name = s3BucketArn.split(':::')[-1]

    try:
        
        # Prepare result code and string
        resultCode = None
        resultString = None
        
        parse.process(bucket_name, file_key, batch=True)

        # Mark as succeeded
        resultCode = 'Succeeded'
        resultString = f'File s3://{bucket_name}/{file_key} has been processed successfully'
        
    except ClientError as e:
        
        # If request timed out, mark as a temp failure
        # and S3 Batch Operations will make the task for retry. If
        # any other exceptions are received, mark as permanent failure.
        errorCode = e.response['Error']['Code']
        errorMessage = e.response['Error']['Message']
        if errorCode == 'RequestTimeout':
            resultCode = 'TemporaryFailure'
            resultString = 'Retry request to Amazon S3 due to timeout.'
        elif errorCode == 'ThrottlingException':
            resultCode = 'TemporaryFailure'
            resultString = 'Retry request due to throttling.'
        elif errorCode == 'TooManyRequestsException':
            resultCode = 'TemporaryFailure'
            resultString = 'Retry request due to throttling.'
        else:
            resultCode = 'PermanentFailure'
            resultString = '{}: {}'.format(errorCode, errorMessage)
            
    except Exception as e:
        
        # Catch all exceptions to permanently fail the task
        resultCode = 'PermanentFailure'
        resultString = 'Exception: {}'.format(e)
        
    finally:
        results.append({
            'taskId': taskId,
            'resultCode': resultCode,
            'resultString': resultString
        })
        
    return {
        'invocationSchemaVersion': invocationSchemaVersion,
        'treatMissingKeysAs': 'PermanentFailure',
        'invocationId': invocationId,
        'results': results
    }
