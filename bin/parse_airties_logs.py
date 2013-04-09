#!/usr/bin/python
#

import re, os
from datetime import datetime, date, time
import redis
import time
import traceback
from hotqueue import HotQueue

#make redis comnnection
r_server = redis.Redis("localhost")
queue = HotQueue("logqueue", host="localhost", port=6379, db=1)
lineNo=0

def matchmyregex(line):
	expireParsedLog = 2764800 # 32 days
	expireIPtoMAC = 259200 # 3 days
	expireRAWlogs = 95040 # 1.1 days

	if not REGM_oldfw.search(line):
		#generate uniq key to combine multiple loglines from same STB (mac + datetime)
		macaddr = REGEXmac.findall(line)
		datetimeUnix = REGEXdatetimeServer.findall(line)[0]
		if  macaddr:
			macNoDelimtTMP = macaddr[0].replace(':', "")
			macNoDelimt = macNoDelimtTMP.replace(" ", "")
	
			datetimeUnix = str((int(datetimeUnix)+120)/300*300) #round to strict 5 min interval
			dateMac = datetimeUnix + macNoDelimt
			r_server.hset(dateMac, "stime", datetimeUnix)
			dateMacLog = 'log' + dateMac

			r_server.sadd('who' + datetimeUnix, macNoDelimt) #adds to list af MACs active within this 5 min window
			r_server.expire('who' + datetimeUnix, expireParsedLog)

			r_server.hset(dateMacLog, lineNo, line) #adds raw log to redis
			r_server.expire(dateMacLog, expireRAWlogs)

			ip = line.split(' ')[1]
			r_server.hset(dateMac, "ip", ip)

			if REGM_ipaddress.search(line):
				firmware = REGEXip.findall(line)
				if len(firmware) > 2:
					ipAton = reduce(lambda x,y: (x<<8) + y, [ int(x) for x in firmware[2].split('.') ])
					r_server.set(ipAton, macNoDelimt)
					r_server.expire(ipAton, expireIPtoMAC)
					r_server.hset(dateMac, "fw", firmware[1])
					r_server.hset(dateMac, "mac", macNoDelimt)
				else:
					r_server.hset(dateMac, "mac", macNoDelimt)

				r_server.expire(dateMac, expireParsedLog)

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
				r_server.hset(dateMac, "upt", upt)
				r_server.expire(dateMac, expireParsedLog)

			elif REGM_uptime_sec.findall(line):
				uptTMP = REGEXupSec.findall(line)
				if uptTMP:
					upt = REGEXupSecDetail.findall(uptTMP[0])[0]
					r_server.hset(dateMac, "uptSec", upt)
					r_server.expire(dateMac, expireParsedLog)

			elif REGM_playing.search(line):
				if REGEXplayurl.search(line):
					playurl = REGEXplayurl.findall(line)
					r_server.hset(dateMac, "url", playurl[0].split('/')[2])
				elif REGEXip.search(line):
					playurl = REGEXip.findall(line)
					if (len(playurl) > 1):
						r_server.hset(dateMac, "url", playurl[1])
					else:
						r_server.hset(dateMac, "url", "unknown")
				else:
					playurl = REGEXplayurl.findall(line)
					r_server.hset(dateMac, "fw", playurl[0])

				r_server.expire(dateMac, expireParsedLog)

			elif REGM_decodeErr.search(line):
				dErr = REGEXdecodeerr.findall(line)
				dErrOflow = dErr[0].split()
				dErrDrops = dErr[1].split()
				operacrash = dErr[2].split();
				dErrII = REGEXdecodeerrII.findall(line)
				dErrErrors = dErrII[0]
				r_server.hset(dateMac, "operacrash", operacrash[1])
				r_server.hset(dateMac, "decodeOflow", dErrOflow[1])
				r_server.hset(dateMac, "ddecodeDrops", dErrDrops[1])
				r_server.hset(dateMac, "decodeErr", dErrErrors[1:-1])
				r_server.expire(dateMac, expireParsedLog)

			elif REGM_display.search(line):
				displayErr = REGEXdecodeerr.findall(line)
				displayUflow = displayErr[0].split();
				displayDrops = displayErr[1].split();
				displayErrII = REGEXdecodeerrII.findall(line)
				displayErrors = displayErrII[0]
				r_server.hset(dateMac, "displayUflow", displayUflow[1])
				r_server.hset(dateMac, "displayDrops", displayDrops[1])
				r_server.hset(dateMac, "displayErr", displayErrors[1:-1])
				r_server.expire(dateMac, expireParsedLog)

			elif REGM_pts.search(line):
				ptsErr = REGEXdecodeerr.findall(line)
				ptsError = ptsErr[0].split()
				Discontinuity = ptsErr[1].split()
				r_server.hset(dateMac, "ptsError", ptsError[1])
				r_server.hset(dateMac, "Discontinuity", Discontinuity[1])
				r_server.expire(dateMac, expireParsedLog)

			elif REGM_stalled.search(line):
				stalledErr = REGEXdecodeerr.findall(line)
				stalled = stalledErr[0].split()
				iframeErr = stalledErr[1].split()
				badStream = stalledErr[2].split()
				r_server.hset(dateMac, "stalled", stalled[1])
				r_server.hset(dateMac, "iframeErr", iframeErr[1])
				r_server.hset(dateMac, "badStream", badStream[1])
				r_server.expire(dateMac, expireParsedLog)

			elif REGM_rtsplog.search(line):
				r_server.hset(dateMac, "mac", macNoDelimt)
				if REGEX_rtsp_died.search(line):
					r_server.hset(dateMac, "rtsperr", "stream died")
				elif REGEX_rtsp_end.search(line):
					r_server.hset(dateMac, "rtsperr", "end of stream")
				elif REGEX_rtsp_fail.search(line):
					r_server.hset(dateMac, "rtsperr", "Connection Failed")
				elif REGEX_rtsp_command.search(line):
					r_server.hset(dateMac, "rtsperr", "command cannot be sent")
				elif REGEX_rtsp_response.search(line):
					r_server.hset(dateMac, "rtsperr", "RTSP command could not read")
				elif REGEX_rtsp_asset.search(line):
					r_server.hset(dateMac, "rtsperr", "asset not found")
				elif REGEX_rtsp_video.search(line):
					r_server.hset(dateMac, "rtsperr", "does not exist")
				elif REGEX_rtsp_server_stop.search(line):
					r_server.hset(dateMac, "rtsperr", "server stopped the connection")
				elif REGEX_rtsp_server_auth.search(line):
					r_server.hset(dateMac, "rtsperr", "server authentication err")
				elif REGEX_rtsp_further.search(line):
					r_server.hset(dateMac, "rtsperr", "Further action")

				r_server.expire(dateMac, expireParsedLog)

			elif REGM_mcast.search(line):
				r_server.hset(dateMac, "mcast", 1)
				r_server.hset(dateMac, "mac", macNoDelimt)
				r_server.expire(dateMac, expireParsedLog)

			elif REGM_invalid.search(line):
				r_server.hset(dateMac, "invaliddata", 1)
				r_server.hset(dateMac, "mac", macNoDelimt)
				r_server.expire(dateMac, expireParsedLog)

			#else:
				#print line
				#r_server.zadd('badlines', line, datetimeUnix)
				#r_server.expire('badlines', 1800)
		else:
			print line


#if match
REGM_oldfw = re.compile(r"\#033")
REGM_ipaddress = re.compile(r"IP addr")
REGM_playing = re.compile(r"video playing")
REGM_decodeErr = re.compile(r"DECODE ")
REGM_display = re.compile(r"DISPLAY ")
REGM_rtsplog = re.compile(r"RTSPErrorLogger")
REGM_pts = re.compile(r"Pts ")
REGM_stalled = re.compile(r"Stalled")
REGM_uptime = re.compile(r"average")
REGM_uptime_sec = re.compile(r"log_uptime")
REGM_mcast = re.compile(r"mcast")
REGM_invalid = re.compile(r"invalid data received")

#extract this
REGEXupSec = re.compile(r"(S : \d+.\d+)")
REGEXupSecDetail = re.compile(r"(\d+)")
REGEXupMin = re.compile(r"(up \d+)")
REGEXupHourMin = re.compile(r"(up +\d+:\d+)")
REGEXupDays = re.compile(r"(up \d+ day)")
REGEXdatetimeSTB = re.compile(r"(\d+-\d+-\d+\s\d+:\d+:\d+)")
REGEXdatetimeServer = re.compile(r"(^\d{10})")
REGEXip = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
REGEXmac = re.compile(r"([\dA-F]{2}:[\dA-F]{2}:[\dA-F]{2}:[\dA-F]{2}:[\dA-F]{2}:[\dA-F]{2})")
REGEXplayurl = re.compile(r"([\a-z]{3,4}://[A-Za-z0-9_\.-]+)")
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

##read redis:
if __name__ == "__main__":
	for line in queue.consume():
		lineClean = line.split('@')[1]
		lineNo = line.split('@')[0]
		try:
			matchmyregex(lineClean)
		except:
			print lineClean
			print traceback.format_exc()
			pass
