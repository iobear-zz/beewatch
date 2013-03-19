#!/usr/bin/python
#
#*/5 * * * * /home/beeadmin/beewatch/bin/generateStats.py >/dev/null 2>&1
#

import os
import datetime
from datetime import datetime, date, time
from time import sleep
import redis
import time

r_server = redis.Redis("localhost")


def countKeys(searchString):
    channels = []
    setTopBox = r_server.keys(searchString)
    setTopBoxAmount = len(setTopBox)

    for key in setTopBox:
        url = r_server.hget(key, "url")
        if url:
            channels.append(url)

    redisKeyNameChannels = 'statsChannel' + searchString.split('*')[0]
    redisKeyNameBoxes = 'statsBoxes' + searchString.split('*')[0]
    redisChannels = dict(dupli(channels))
    r_server.hmset(redisKeyNameChannels, redisChannels)
    r_server.expire(redisKeyNameChannels, 2764800)  # 32 days
    r_server.set(redisKeyNameBoxes, setTopBoxAmount)
    r_server.expire(redisKeyNameBoxes, 2764800)  # 32 days

def dupli(the_list):
    count = the_list.count
    result = [(item, count(item)) for item in set(the_list)]
    result.sort()
    return result

#initiate stats, find 5 min timeframe to work with
if __name__ == "__main__":
    sleep(3)
    timeNow = time.time()
    datetimeUnix = str((int(timeNow)+120)/300*300)  # round to strict 5 min interval
    searchString = str(int(datetimeUnix) - 300) + "*"  # search the previous 5 min interval
    countKeys(searchString)
