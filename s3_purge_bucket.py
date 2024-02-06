#!/usr/bin/python3

import boto3
import os

from argparse import ArgumentParser

access_key = 'XXX'
secret_key = 'YYYYYYYYYY'

rgw_endpoint_primary = 'http://ENDPOINT:80'

parser = ArgumentParser(description='Purges objects in the specified bucket')
parser.add_argument('--bucket-name',
	dest='bucket_name',
	action='store',
	required=True,
	help='target bucket for purging')
parser.add_argument('--max-delete',
	dest='max_delete',
	action='store',
	required=True,
	help='maximum number of deleted objects')
args = parser.parse_args()

s3 = boto3.resource('s3',
        endpoint_url=rgw_endpoint_primary,
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	)


def purge_bucket(Bucket, S3Client, MaxDelete):
    total_deleted = 0
    response = S3Client.meta.client.list_objects_v2(Bucket=Bucket)
    while 'Contents' in response and response['KeyCount'] > 0:
        for key in response['Contents']:
            value = key['Key']
            key.clear()
            key['Key'] = value
        count = len(response["Contents"])
        total_deleted = total_deleted + count
        if total_deleted > MaxDelete:
            print(f'Maximum number of keys reached, exit.')
            return
        print(f'Deleting {count} keys at {Bucket}')
        out = S3Client.meta.client.delete_objects(
            Bucket=Bucket, 
            Delete={'Objects': response['Contents']}
        )
        if 'Errors' in out:
            print(f'Errors at {Bucket}: {out["Errors"]}')
        response = S3Client.meta.client.list_objects_v2(Bucket=Bucket)
    return Bucket

purge_bucket(Bucket=args.bucket_name,S3Client=s3,MaxDelete=int(args.max_delete))

