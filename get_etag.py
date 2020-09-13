# Rough script created to get the ETag of the object

import boto
import boto.s3.connection

# Specify acces_key and secret_key from RGW user
access_key = $access 
secret_key = $secret

# Specify rgw hostname and port
rgw_hostname = ""
rgw_port = 8080

conn = boto.connect_s3(
aws_access_key_id = access_key,
aws_secret_access_key = secret_key,
host = rgw_hostname,
port = rgw_port,
is_secure=False,
calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)

# Pass the filename which exists 
file_name = 'foo.txt'

for bucket in conn.get_all_buckets():
    print( bucket.name, bucket.creation_date, " ", bucket.get_key(file_name).etag[1:-1])
