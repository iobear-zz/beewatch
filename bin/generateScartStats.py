#!/usr/bin/python
#

import time
import datetime
from datetime import datetime
import redis
import re

r_server = redis.Redis(host='localhost', port=6380, db=0)
r_server_raw = redis.Redis(host='localhost', port=6379, db=0)


def countKeys(datetimeUnix):
    counter = 1
    searchString = datetimeUnix
    oldSearchString = "string"

    while counter != 18:
        print 'adding customers from ' + str(datetime.fromtimestamp(int(searchString)))

        if countKeys == 1:
            setTopBox = r_server.smembers('who' + searchString)
        else:
            setTopBox = r_server.sdiff('who' + searchString, 'who' + oldSearchString)

        for key in setTopBox:
            r_server.sadd('who24' + datetimeUnix, key)

        counter += 1
        oldSearchString = searchString
        searchString = str(int(searchString) - 5400)  # search the previous 2h interval


def findHDMIcustomers(datetimeUnix):
    loglinesSearched = 0
    searchString = datetimeUnix
    REGEXhdmiSearch = re.compile(r"HDMI: connected")
    counter = 1

    setTopBoxs24h = r_server.smembers('who24' + datetimeUnix)

    while counter != 18:

        for key in setTopBoxs24h:
            rawLog = r_server_raw.hvals('log' + searchString + key)
            if rawLog:
                for rawLogString in rawLog:
                    loglinesSearched += 1
                    if REGEXhdmiSearch.search(rawLogString):
                        r_server.srem('who24' + datetimeUnix, key)
                        break

        searchString = str(int(searchString) - 5400)  # search the previous 2h interval
        print 'Searching the remaning ' + str(len(r_server.smembers('who24' + datetimeUnix))) + ' Customers not using HDMI at ' + str(datetime.fromtimestamp(int(searchString)))
        counter += 1

    print str(len(r_server.smembers('who24' + datetimeUnix))) + ' Customers is not using HDMI'
    print "searched " + str(loglinesSearched) + " loglines"

#initiate stats, find 5 min timeframe to work with
if __name__ == "__main__":
    timeNow = time.time()

    #first find all atcive boxes for the last 24 hours
    counter = 1
    datetimeUnix = str((int(timeNow)+120)/300*300)  # round to strict 5 min interval
    searchString = str(int(datetimeUnix) - 300)  # search the previous 5 min interval

    countKeys(searchString)

    print str(len(r_server.smembers('who24' + searchString))) + ' Customers to search'

    findHDMIcustomers(searchString)
