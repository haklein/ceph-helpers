#!/usr/bin/python
#
# iterates over buckets and compares the md5 checksum across objects on primary and secondary connection
#

import sys
import re

import boto3

access_key = 'XXXXXXXXXXXXXXXXXXXX'
secret_key = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

rgw_endpoint_primary = 'http://primary:80'
rgw_endpoint_secondary  = 'http://secondary:80'

# when all_buckets is set to true, the script will iterate over all buckets
all_buckets = True
# when it is set to false, the bucket name needs to be specified:
single_bucket_name = 'test2'

compare_dicts = True

conn_primary = boto3.client('s3',
        endpoint_url=rgw_endpoint_primary,
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	)

conn_secondary = boto3.client('s3',
        endpoint_url=rgw_endpoint_secondary,
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	)


def bucket2list(s3, bucket_name):
    result = {}
    response = s3.list_objects_v2(Bucket=bucket_name)
    while True:
        for item in response['Contents']:
            result[item['Key']]=item['ETag']
        if not response['IsTruncated']:
            break;
        print("Paging results: ", response['NextContinuationToken'])
        response = s3.list_objects_v2(Bucket=bucket_name,ContinuationToken=response['NextContinuationToken'])
    return result

if all_buckets:
    bucketlist = conn_primary.list_buckets()
else:
    bucketlist = {'Buckets':[{'Name':single_bucket_name}]}

for bucket in bucketlist['Buckets']:
    print("Bucket: ", bucket['Name'])
    bucketlist_primary = bucket2list(conn_primary, bucket['Name'])
    try:
        # bucketlist_secondary = bucket2list(conn_secondary, 'test3')
        bucketlist_secondary = bucket2list(conn_secondary, bucket['Name'])
        for item in bucketlist_primary:
            print ("P",item, bucketlist_primary[item])
            if item in bucketlist_secondary:
                print ("S", item, bucketlist_secondary[item])
                if bucketlist_primary[item] != bucketlist_secondary[item]:
                    print ("ERROR: MD5 mismatch", item, bucketlist_primary[item], bucketlist_secondary[item])
            else:
                print ("ERROR: no such object on secondary: ", item)
        if compare_dicts:
            if bucketlist_primary == bucketlist_secondary:
                print("Buckets do match")
            else:
                print("Buckets do not match")

    except Exception as e:
        if re.search("NoSuchBucket", str(e)):
            print ("ERROR: bucket does not exist on secondary: ", bucket['Name'])
        else:
            print ("ERROR: unable to validate object on secondary, Exception: ", e)
