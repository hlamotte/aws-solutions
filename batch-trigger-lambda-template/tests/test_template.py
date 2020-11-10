import unittest
import lambda_s3_create 
import lambda_s3_batch

# test file on S3:
bucket_name = "your-bucket"
key = "test-file-key"


class TestLambdas(unittest.TestCase):

    def test_batch(self):

        context = None
        event = {
            "invocationSchemaVersion": "1.0",
            "invocationId": "YXNkbGZqYWRmaiBhc2RmdW9hZHNmZGpmaGFzbGtkaGZza2RmaAo",
            "job": {
                "id": "f3cc4f60-61f6-4a2b-8a21-d07600c373ce"
            },
            "tasks": [
                {
                "taskId": "dGFza2lkZ29lc2hlcmUK",
                "s3Key": key,
                "s3VersionId": "1",
                "s3BucketArn": f"arn:aws:s3:::{bucket_name}"
                }
            ]
        }

        expected = {
            'invocationSchemaVersion': '1.0',
            'treatMissingKeysAs': 'PermanentFailure',
            'invocationId': 'YXNkbGZqYWRmaiBhc2RmdW9hZHNmZGpmaGFzbGtkaGZza2RmaAo',
            'results': [{
                'taskId': 'dGFza2lkZ29lc2hlcmUK',
                'resultCode': 'Succeeded',
                'resultString': f'File s3://{bucket_name}/{key} has been processed successfully'
            }]
        }

        response = lambda_s3_batch.lambda_handler(event, context)
        #self.assertEqual(response, expected)

    def test_create(self):

        context = None
        event = {
            "Records": [
                {
                    "eventVersion": "2.1",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-2",
                    "eventTime": "2019-09-03T19:37:27.192Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "AWS:AIDAINPONIXQXHT3IKHL2"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "205.255.255.255"
                    },
                    "responseElements": {
                        "x-amz-request-id": "D82B88E5F771F645",
                        "x-amz-id-2": "vlR7PnpV2Ce81l0PRw6jlUpck7Jo5ZsQjryTjKlc5aLWGVHPZLj5NeC6qMa0emYBDXOo6QBU0Wo="
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "828aa6fc-f7b5-4305-8584-487c791949c1",
                        "bucket": {
                            "name": bucket_name,
                            "ownerIdentity": {
                                "principalId": "A3I5XTEXAMAI3E"
                            },
                            "arn": f"arn:aws:s3:::{bucket_name}"
                        },
                        "object": {
                            "key": key,
                            "size": 1305107,
                            "eTag": "b21b84d653bb07b05b1e6b33684dc11b",
                            "sequencer": "0C0F6F405D6ED209E1"
                        }
                    }
                }
            ]
        }

        expected = {
            'statusCode': 200,
            'body': f'"File s3://{bucket_name}/{key} has been processed successfully"'
        }

        response = lambda_s3_create.lambda_handler(event, context)
        print(response)
        #self.assertEqual(response, expected)

if __name__ == '__main__':
    unittest.main()
