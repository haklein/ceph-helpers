#!/usr/bin/python3

import boto3
import uuid
import os
import random

from argparse import ArgumentParser

access_key = 'XXX'
secret_key = 'YYYYYYYYYY'

rgw_endpoint_primary = 'http://ENDPOINT:80'

rgw_endpoint_primary = 'http://dell-r330-17:80'

parser = ArgumentParser(description='Creates testobjects in the specified bucket')
parser.add_argument('--bucket-name',
	dest='bucket_name',
	action='store',
	required=True,
	help='target bucket for test objects')
args = parser.parse_args()

s3 = boto3.resource('s3',
        endpoint_url=rgw_endpoint_primary,
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	)

bucket = s3.Bucket(args.bucket_name)
bucket.create()

i=0
while True:
	# random object size 
	size = random.randint(10, 2000) * 1024
	# using uuid as object name, random content
	bucket.put_object(Bucket=args.bucket_name,Key=str(uuid.uuid4()),Body=os.urandom(size))
	i+=1
	if i % 100 == 0:
		print("Generated: ", i)


