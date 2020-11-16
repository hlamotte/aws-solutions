mport json
import csv
import boto3 
import datetime
import urllib
import argparse

            
def get_all_s3_objects(s3, **base_kwargs):
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield response.get('Contents', [])
        if not response.get('IsTruncated'):  # At the end of the list?
            break
        continuation_token = response.get('NextContinuationToken')


my_parser = argparse.ArgumentParser(description='Generate manifest from S3')
# Add the arguments
my_parser.add_argument('bucket_name',
                       type=str,
                       help='Name of S3 bucket containing objects')

my_parser.add_argument('prefix',
                       type=str,
                       help='S3 prefix of objects')

my_parser.add_argument('suffix',
                       type=str,
                       help='Suffix of objects')

my_parser.add_argument('manifest_bucket',
                       type=str,
                       help='Suffix of objects')

my_parser.add_argument('manifest_key',
                       type=str,
                       help='Suffix of objects')

args = my_parser.parse_args()
bucket_name = args.bucket_name
prefix = args.prefix
suffix = args.suffix
manifest_bucket = args.manifest_bucket
manifest_key = args.manifest_key

#s3 = boto3.resource('s3')
#bucket = s3.Bucket(bucket_name)
with open('/tmp/temp.csv', 'w', newline='') as outfile:
    #fieldnames = ['setting', 'value', 'path']
    writer = csv.writer(outfile, escapechar='\\', quoting=csv.QUOTE_ALL)
    gen = get_all_s3_objects(boto3.client('s3'), Bucket=bucket_name, Prefix=prefix)
    for pidx, page in enumerate(gen):  #, Prefix=prefix):
        #print('Page: ', len(page))
        for idx, file in enumerate(page):
            #print(file_i)
            if file['Key'].endswith(suffix):
                key = urllib.parse.quote(file['Key'])
                writer.writerow([bucket_name, key]) 
            #print('File: ', file['Key'])
            #print(idx)
        print(f'Processing page {pidx}')  
        #if pidx == 2:
        #    break
        #break
print(f"Uploading manfest s3://{manifest_bucket}/{manifest_key}")
now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
target_bucket_name = manifest_bucket
target_file = manifest_key
s3_client = boto3.client('s3') 
s3_client.upload_file(
    '/tmp/temp.csv', target_bucket_name, target_file
)
print(f"Sucessfully uploaded manifest to s3://{manifest_bucket}/{manifest_key}")