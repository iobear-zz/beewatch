#!/usr/bin/python
#

import re, os
import time
from hotqueue import HotQueue

queue = HotQueue("logqueue", host="localhost", port=6379, db=1)
filename = '/dev/shm/logs/air.log'
lineNumber = 1

if __name__ == "__main__":
	ins = open( filename, "r" )
	for line in ins:
		laengde = len(line)
		if laengde > 4:
			newLogString = str(lineNumber) + '@' + line
			queue.put(newLogString)
			lineNumber += 1

file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

while 1:
	where = file.tell()
	line = file.readline()
	if not line:
		time.sleep(1)
		file.seek(where)
	else:
		newLogString = str(lineNumber) + '@' + line
		queue.put(newLogString)
		lineNumber += 1
		if lineNumber > 10000000:
			lineNumber = 1
