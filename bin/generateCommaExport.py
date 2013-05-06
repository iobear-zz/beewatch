#!/usr/bin/python
#
# cron : */5 * * * * /home/beeadmin/beewatch/bin/generateCommaExport.py > /tmp/commaExport.txt
#

import time
import datetime
from datetime import datetime
import redis
import shutil

r_server = redis.Redis(host='localhost', port=6380, db=0)


def printKeys(searchString):
    setTopBox = r_server.smembers('who' + searchString)

    for key in setTopBox:
        mac = key
        isoTime = datetime.fromtimestamp(int(r_server.hget(searchString + key, "stime"))).isoformat()
        ip = r_server.hget(searchString + key, "ip")
        fw = r_server.hget(searchString + key, "fw")
        uptime = r_server.hget(searchString + key, "uptSec")
        url = r_server.hget(searchString + key, "url")
        operacrash = r_server.hget(searchString + key, "operacrash")
        mcast = r_server.hget(searchString + key, "mcast")
        decodeErr = r_server.hget(searchString + key, "decodeErr")
        rtsperr = r_server.hget(searchString + key, "rtsperr")

        if rtsperr == "RTSP server send a end of stream event":
            rtsperr = "None"

        if not mcast:
            mcast = 0

        if not operacrash:
            operacrash = 0

        print str(isoTime) + ',' + str(ip) + ',' + str(fw) + ',' + str(mac) + ',' + str(uptime) + ',' + str(url) + ',' + str(mcast) + ',' + str(operacrash) + ',' + str(decodeErr) + ',' + str(rtsperr)

    dstFile = '/mnt/nfs/dump/' + str(isoTime) + '.txt'
    srcFile = '/tmp/commaExport.txt'
    shutil.copy(srcFile, dstFile)

#initiate stats, find 5 min timeframe to work with
if __name__ == "__main__":
    timeNow = time.time()
    datetimeUnix = str((int(timeNow)+120)/300*300)  # round to strict 5 min interval
    searchString = str(int(datetimeUnix) - 300)  # search the previous 5 min interval
    printKeys(searchString)
