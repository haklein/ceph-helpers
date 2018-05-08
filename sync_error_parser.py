#!/usr/bin/python

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
		# current_type_ts = datetime.strptime(type['time'], '%Y-%m-%d %H:%M:%S.%f') # 2017-01-27 16:25:06.942698
		# if 'last_type_ts' in locals():
		#	delta = current_type_ts - last_type_ts
	#		total_type_duration += delta
		#print "   ", "%d.%.6d" % (total_type_duration.seconds, total_type_duration.microseconds), "%d.%.6d" % (delta.seconds, delta.microseconds), type['event']
		#pprint(type)
