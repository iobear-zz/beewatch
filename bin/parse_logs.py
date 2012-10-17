#!/usr/bin/python
#

import re, os
from datetime import datetime, date, time
import redis
import time
#make redis comnnection
r_server = redis.Redis("localhost")

def matchmyregex(line):
	if not REGM_oldfw.search(line):
		#generate uniq key to combine multiple loglines from same STB (mac + datetime)
		macaddr = REGEXmac.findall(line)
		datetimeTmp = REGEXdatetime.findall(line)
		macNoDelimtTMP = macaddr[0].replace(':', "")
		macNoDelimt = macNoDelimtTMP.replace(" ", "")
	
		datetimeUnixTmp = datetime.strptime(datetimeTmp[0] , "%Y-%m-%d %H:%M:%S").strftime('%s')
		datetimeUnix = str((int(datetimeUnixTmp)+120)/300*300) #round to strict 5 min interval
		dateMac = datetimeUnix + macNoDelimt
		r_server.zadd(dateMac, "stime:" + datetimeUnix, datetimeUnix)
		dateMacLog = 'log' + datetimeUnix + macNoDelimt
		r_server.zadd(dateMacLog, line, datetimeUnix)
		r_server.expire(dateMacLog, 864000)
		if REGM_ipaddress.search(line):
			firmware = REGEXip.findall(line)
			if len(firmware) > 2:
				ipAton = reduce(lambda x,y: (x<<8) + y, [ int(x) for x in firmware[2].split('.') ])
#				r_server.zadd(macNoDelimt, firmware[2], ipAton)
#				r_server.expire(macNoDelimt, 432000)
				r_server.set(ipAton, macNoDelimt)
				r_server.expire(ipAton, 432000)
				r_server.zadd(dateMac, "fw:" + firmware[1], datetimeUnix)
				r_server.zadd(dateMac, "ip:" + firmware[2], datetimeUnix)
				r_server.zadd(dateMac, "mac:" + macNoDelimt, datetimeUnix)
			else:
				r_server.zadd(dateMac, "ip:" + firmware[1], datetimeUnix)
				r_server.zadd(dateMac, "mac:" + macNoDelimt, datetimeUnix)				
		elif REGM_uptime.search(line):
			uptTMP = REGEXupDays.findall(line)
			minDag = 1
			if (uptTMP):
				minDag = 10000
			if not (uptTMP):
				uptTMP = REGEXupHourMin.findall(line)
			if not (uptTMP):
				uptTMP = REGEXupMin.findall(line)
			upt = uptTMP[0].split()[1].replace(':', "") #remove "up", space & :
			upt = str(int(upt) * minDag)
			r_server.zadd(dateMac, "upt:" + upt, datetimeUnix)
		elif REGM_playing.search(line):
			if REGEXplayurl.search(line):
				playurl = REGEXplayurl.findall(line)
				r_server.zadd(dateMac, "url:" + playurl[0].split('/')[2], datetimeUnix)				
			elif REGEXip.search(line):
				playurl = REGEXip.findall(line)
				if (len(playurl) > 1):
					r_server.zadd(dateMac, "url:" + playurl[1], datetimeUnix)
				else:
					r_server.zadd(dateMac, "url:unknown", datetimeUnix)				
			else:
				playurl = REGEXplayurl.findall(line)
				r_server.zadd(dateMac, "fw:" + playurl[0], datetimeUnix)
#		elif REGM_memory.search(line):
#			memory = REGEXmem.findall(line)
#			memTotal = memory[0].split() #Total Mem
#			memFree = memory[1].split() #Free Memory
#			kernelCached = memory[2].split() #Kernel Cached
#			kernelFree = memory[3].split() #Kernel free
#			r_server.zadd(dateMac, "memTotal:" + memTotal[0], datetimeUnix)
#			r_server.zadd(dateMac, "memFree:" + memFree[0], datetimeUnix)
#			r_server.zadd(dateMac, "kernelFree:" + kernelFree[0], datetimeUnix)
#			r_server.zadd(dateMac, "kernelCached:" + kernelCached[0], datetimeUnix)
		elif REGM_decodeErr.search(line):
			dErr = REGEXdecodeerr.findall(line)
			dErrOflow = dErr[1].split()
			dErrDrops = dErr[2].split()
			operacrash = dErr[3].split();
			dErrII = REGEXdecodeerrII.findall(line)
			dErrErrors = dErrII[0]
			r_server.zadd(dateMac, "operaCrash:" + operacrash[1], datetimeUnix)
			r_server.zadd(dateMac, "decodeOflow:" + dErrOflow[1], datetimeUnix)
			r_server.zadd(dateMac, "ddecodeDrops:" + dErrDrops[1], datetimeUnix)
			r_server.zadd(dateMac, "decodeErr:" + dErrErrors[1:-1], datetimeUnix)
		elif REGM_display.search(line):
			displayErr = REGEXdecodeerr.findall(line)
			displayOflow = displayErr[1].split();
			displayDrops = displayErr[2].split();
			displayErrII = REGEXdecodeerrII.findall(line)
			displayErrors = displayErrII[0]
			r_server.zadd(dateMac, "displayOflow:" + displayOflow[1], datetimeUnix)
			r_server.zadd(dateMac, "displayDrops:" + displayDrops[1], datetimeUnix)
			r_server.zadd(dateMac, "displayErr:" + displayErrors[1:-1], datetimeUnix)
		elif REGM_pts.search(line):
			ptsErr = REGEXdecodeerr.findall(line)
			ptsOflow = ptsErr[1].split()
			ptsDrops = ptsErr[2].split()
			r_server.zadd(dateMac, "ptsOflow:" + ptsOflow[1], datetimeUnix)
			r_server.zadd(dateMac, "ptsDrops:" + ptsDrops[1], datetimeUnix)
		elif REGM_stalled.search(line):
			stalledErr = REGEXdecodeerr.findall(line)
			stalled = stalledErr[1].split()
			iframeErr = stalledErr[2].split()
			badStream = stalledErr[3].split()
			r_server.zadd(dateMac, "stalled:" + stalled[1], datetimeUnix)
			r_server.zadd(dateMac, "iframeErr:" + iframeErr[1], datetimeUnix)
			r_server.zadd(dateMac, "badStream:" + badStream[1], datetimeUnix)
		elif REGM_rtsplog.search(line):
			r_server.zadd(dateMac, "mac:" + macNoDelimt, datetimeUnix)
			if REGEX_rtsp_died.search(line):
				r_server.zadd(dateMac, "rtsperr:stream died", datetimeUnix)
			elif REGEX_rtsp_end.search(line):
				r_server.zadd(dateMac, "rtsperr:end of stream", datetimeUnix)
			elif REGEX_rtsp_fail.search(line):
				r_server.zadd(dateMac, "rtsperr:Connection Failed", datetimeUnix)
			elif REGEX_rtsp_command.search(line):
				r_server.zadd(dateMac, "rtsperr:command cannot be sent", datetimeUnix)
			elif REGEX_rtsp_response.search(line):
				r_server.zadd(dateMac, "rtsperr:RTSP command could not read", datetimeUnix)
			elif REGEX_rtsp_asset.search(line):
				r_server.zadd(dateMac, "rtsperr:asset not found", datetimeUnix)
			elif REGEX_rtsp_video.search(line):
				r_server.zadd(dateMac, "rtsperr:does not exist", datetimeUnix)
			elif REGEX_rtsp_server_stop.search(line):
				r_server.zadd(dateMac, "rtsperr:server stopped the connection", datetimeUnix)
			elif REGEX_rtsp_server_auth.search(line):
				r_server.zadd(dateMac, "rtsperr:server authentication err", datetimeUnix)
			elif REGEX_rtsp_further.search(line):
				r_server.zadd(dateMac, "rtsperr:Further action", datetimeUnix)
		elif REGM_mcast.search(line):
			r_server.zadd(dateMac, "mcast:1", datetimeUnix)
			r_server.zadd(dateMac, "mac:" + macNoDelimt, datetimeUnix)
		elif REGM_invalid.search(line):
			r_server.zadd(dateMac, "invaliddata:1", datetimeUnix)
			r_server.zadd(dateMac, "mac:" + macNoDelimt, datetimeUnix)
			#		else:
#			r_server.zadd('badlines', line, datetimeUnix)

#if match
REGM_oldfw = re.compile(r"\#033")
REGM_ipaddress = re.compile(r"IP addr")
REGM_playing = re.compile(r"video playing")
REGM_decodeErr = re.compile(r"DECODE ")
REGM_display = re.compile(r"DISPLAY ")
REGM_rtsplog = re.compile(r"RTSPErrorLogger")
REGM_pts = re.compile(r"Pts ")
REGM_stalled = re.compile(r"Stalled")
REGM_memory = re.compile(r"Memory")
REGM_uptime = re.compile(r"average")
REGM_mcast = re.compile(r"mcast")
REGM_invalid = re.compile(r"invalid data received")
#extract this

REGEXupMin = re.compile(r"(up \d+)")
REGEXupHourMin = re.compile(r"(up +\d+:\d+)")
REGEXupDays = re.compile(r"(up \d+ day)")
REGEXdatetime = re.compile(r"(\d+-\d+-\d+\s\d+:\d+:\d+)")
REGEXip = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
REGEXmac = re.compile(r"([\dA-F]{2}: [\dA-F]{2}:[\dA-F]{2}:[\dA-F]{2}:[\dA-F]{2}:[\dA-F]{2})")
REGEXplayurl = re.compile(r"([\a-z]{3,4}://[A-Za-z0-9_\.-]+)")
REGEXmem = re.compile(r"\d+\skB")
REGEXdecodeerr = re.compile(r":\s\d+")
REGEXdecodeerrII = re.compile(r":\d+,")
REGEX_serial = re.compile(r"Serial")
REGEX_rtsp_end = re.compile(r"end of stream")
REGEX_rtsp_died = re.compile(r"connection died")
REGEX_rtsp_fail = re.compile(r"Connection Failed")
REGEX_rtsp_command = re.compile(r"command cannot")
REGEX_rtsp_response = re.compile(r"Response to RTSP")
REGEX_rtsp_asset = re.compile(r"Asset was")
REGEX_rtsp_video = re.compile(r"does not exist")
REGEX_rtsp_server_stop = re.compile(r"server stopped the connection")
REGEX_rtsp_server_auth = re.compile(r"authentication")
REGEX_rtsp_further = re.compile(r"Further")

##read files:

if __name__ == "__main__":
	ins = open( "/dev/shm/logs/air.log", "r" )
	for line in ins:
		laengde = len(line)
		if laengde > 4:
			# print line
			matchmyregex(line)

filename = '/dev/shm/logs/air.log'
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
		matchmyregex(line)
		#print line, # already has newline
