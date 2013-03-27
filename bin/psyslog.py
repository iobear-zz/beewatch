#!/usr/bin/python

## Tiny Syslog Server in Python.
##
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a HotQueue in Redis
#
#Org file at https://gist.github.com/marcelom/4218010
#

import SocketServer
import time
from hotqueue import HotQueue

queue = HotQueue("logqueue", host="localhost", port=6379, db=1)
HOST, PORT = "0.0.0.0", 514

lineNumber = 1

class SyslogUDPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		global lineNumber
		data = bytes.decode(self.request[0].strip())

		laengde = len(data)
		if laengde > 4:
			newLogString = "%s@%s %s %s\n" % (lineNumber, int(time.time()), self.client_address[0], data)
			queue.put(newLogString)
			lineNumber += 1

		if lineNumber > 10000000:
			lineNumber = 1

if __name__ == "__main__":
	try:
		server = SocketServer.UDPServer((HOST, PORT), SyslogUDPHandler)
		server.serve_forever()
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
