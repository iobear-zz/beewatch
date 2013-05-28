#!/usr/bin/python
#
# cron : */5 * * * * /home/beeadmin/beewatch/bin/generateCommaExport.py > /tmp/commaExport.txt
#

import time
import datetime
from datetime import datetime
import redis
import shutil
import re

r_server = redis.Redis(host='localhost', port=6380, db=0)


def printKeys(searchString):
    setTopBox = r_server.smembers('who' + searchString)
    endOfStream = re.compile(r"RTSP server send a end of stream event")

    for key in setTopBox:
        mac = key
        ip = r_server.hget(searchString + key, "ip")
        fw = r_server.hget(searchString + key, "fw")
        uptime = r_server.hget(searchString + key, "uptSec")
        url = r_server.hget(searchString + key, "url")
        operacrash = r_server.hget(searchString + key, "operacrash")
        mcast = r_server.hget(searchString + key, "mcast")
        decodeErr = r_server.hget(searchString + key, "decodeErr")
        rtsperr = r_server.hget(searchString + key, "rtsperr")
        if r_server.hget(searchString + key, "stime"):
            isoTime = datetime.fromtimestamp(int(r_server.hget(searchString + key, "stime"))).isoformat()

        if rtsperr:
            if endOfStream.search(rtsperr):
                rtsperr = "None"

        if not mcast:
            mcast = 0

        if not operacrash:
            operacrash = 0

        print str(isoTime) + ',' + str(ip) + ',' + str(fw) + ',' + str(mac) + ',' + str(uptime) + ',' + str(url) + ',' + str(mcast) + ',' + str(operacrash) + ',' + str(decodeErr) + ',' + str(rtsperr)

    dstFileTMP = '/mnt/nfs/dump/' + str(isoTime) + '.txt'
    dstFileTMP = dstFileTMP.split(":")
    dstFile = dstFileTMP[0] + dstFileTMP[1] + dstFileTMP[2]
    srcFile = '/tmp/commaExport.txt'
    shutil.copy(srcFile, dstFile)

#initiate stats, find 5 min timeframe to work with
if __name__ == "__main__":
    timeNow = time.time()
    datetimeUnix = str((int(timeNow)+120)/300*300)  # round to strict 5 min interval
    searchString = str(int(datetimeUnix) - 300)  # search the previous 5 min interval
    printKeys(searchString)
