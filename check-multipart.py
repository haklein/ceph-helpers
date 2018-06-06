#!/usr/bin/python
#
# iterates over buckets and lists mulitpart uploads
#

import sys

import boto
import boto.s3.connection
from boto.s3.key import Key

access_key = '3M6MPJ81AK4VR7QVK62Y'
secret_key = 'eBi3w3d2YfpMDEADzquo8XXCgVSWNtRkvFSiZgUg'
rgw_hostname = 'my-s3-endpoint'
rgw_port = 8080

conn = boto.connect_s3(
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	host = rgw_hostname,
	port = rgw_port,
	is_secure=False,
	calling_format = boto.s3.connection.OrdinaryCallingFormat(),
	)

for bucket in conn.get_all_buckets():
	print "{name}\t{created}".format( name = bucket.name, created = bucket.creation_date,)
	print "Multipart uploads: ", bucket.get_all_multipart_uploads()
  
