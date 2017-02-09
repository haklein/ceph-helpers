#!/usr/bin/python

import json
import sys
from datetime import datetime
from pprint import pprint

max_duration = 0.0
total_ops = 0
total_duration = 0.0

if len(sys.argv) != 2:
	print "please specify a file as argument"
	exit

with open(sys.argv[1]) as ops_file:
	ops_data = json.load(ops_file)

for op in ops_data['Ops']:
	print op['duration'], op['description']
	if op['duration'] > max_duration:
		max_duration = op['duration']
	# pprint(op)	
	total_ops = total_ops + 1
	total_duration += op['duration']
	for type in op['type_data'][2]:
		current_type_ts = datetime.strptime(type['time'], '%Y-%m-%d %H:%M:%S.%f') # 2017-01-27 16:25:06.942698
		if 'last_type_ts' in locals():
			delta = current_type_ts - last_type_ts
			total_type_duration += delta
		else: # first iteration
			delta = current_type_ts - current_type_ts
			total_type_duration = delta
			print "   ", type['time']
		last_type_ts = current_type_ts	
		print "   ", "%d.%.6d" % (total_type_duration.seconds, total_type_duration.microseconds), "%d.%.6d" % (delta.seconds, delta.microseconds), type['event']
		#pprint(type)
	del last_type_ts
	del total_type_duration
print "Max duration: ", max_duration
print "Avg duration: ", total_duration / total_ops
