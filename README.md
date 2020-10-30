# AWS Solutions
Useful solutions for working with AWS.

## Generate S3 Manifest
For creating a csv manifest list of all files in an S3 bucket with a certain prefix and suffix. 
- Compatible for use with S3 Batch Operations.
- Manfest uses bucket, key schema.
- Manifest is uploaded to a target location on S3.

Executing from the CLI:
```
$ python generate_manifest.py bucket_name prefix suffix manifest_bucket manifest_key
```

Example:
```
$ python generate_manifest.py my-bucket path/to/data/2020-09-24/ .xml manifest-bucket 2020-10-26_manifest.csv
```