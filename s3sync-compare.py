#!/usr/bin/python
#
# iterates over buckets and compares the md5 checksum across objects on primary and secondary connection
#

import sys
import re

import boto
import boto.s3.connection
from boto.s3.key import Key

access_key = '3M6MPJ81AK4VR7QVK62I'
secret_key = 'eBi3w3d2YfpMoquGzquo8YXCgVSWNtRkvFSiZgUg'
rgw_hostname_primary = 'rdh-cu-8'
rgw_hostname_secondary  = 'rdh-cu-8'
rgw_port = 8080

conn_primary = boto.connect_s3(
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	host = rgw_hostname_primary,
	port = rgw_port,
	is_secure=False,
	calling_format = boto.s3.connection.OrdinaryCallingFormat(),
	)

conn_secondary = boto.connect_s3(
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	host = rgw_hostname_secondary,
	port = rgw_port,
	is_secure=False,
	calling_format = boto.s3.connection.OrdinaryCallingFormat(),
	)

for bucket in conn_primary.get_all_buckets():
	print "{name}\t{created}".format( name = bucket.name, created = bucket.creation_date,)
	rs_keys = bucket.get_all_keys()
	for key_val in rs_keys:
		print "P",key_val, key_val.name, key_val.etag
		try:
			bucket_secondary = conn_secondary.get_bucket(bucket.name)
			key_secondary = bucket_secondary.get_key(key_val.name)
			if key_secondary == None:
				print "ERROR: object does not exist on secondary: ", key_val
			else:
				print "S", key_secondary, key_secondary.name, key_secondary.etag
				if key_val.etag != key_secondary.etag:
					print "ERROR: MD5 mismatch", key_val, key_val.etag, key_secondary.etag
		except Exception, e:
			if re.search("404", str(e)):
				print "ERROR: bucket does not exist on secondary: ", bucket.name
			else:
				print "ERROR: unable to validate object on secondary: ", key_val, " Exception: ", e


