#!/usr/bin/python
#
# something similar can be achieved with:
# jq -r '.[].entries[] | [.timestamp, .info.error_code, .info.message, .name] | @csv'

import json
import sys
from datetime import datetime
from pprint import pprint


if len(sys.argv) != 2:
	print "please specify a file as argument"
	exit

with open(sys.argv[1]) as error_list_file:
	error_list = json.load(error_list_file)

for shard in error_list:
	shard_id = shard['shard_id']

	for entry in shard['entries']:
		print entry['timestamp'], shard_id, entry['section'], '"' + entry['name'] + '"', entry['info']['error_code'], '"' + entry['info']['message'] + '"'
