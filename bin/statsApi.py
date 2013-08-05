#!/usr/bin/python
#

from bottle import route, run, request, abort
import redis
import time
import json

r_server = redis.Redis(host='localhost', port=6380, db=0)

IPranges = ['1023', '1037', '1038', '1039', '1044', '1045', '1049', '1050', '1051', '1055', '1056', '1061', '10200', '10221', '10230', '7768', '87104', '17228']


@route('/v1/stats/err/:type/:callback', method='GET')
def getDecodeErr(type, callback):
    errPrBoxArr = []
    htmlErrArr = {}

    searchString = 'IP16' + getCurretTime()

    for key in IPranges:
        decodeErr = r_server.hget(searchString + key, type)
        totalOnline = r_server.hget(searchString + key, 'totalOnline')

        if decodeErr:
            errPrBox = round(float(decodeErr)/float(totalOnline), 4)
            errPrBox = str(round(errPrBox, 3))
            errPrBoxArr.append(errPrBox)
        else:
            errPrBoxArr.append('0')

    i = 0
    for i, elem in enumerate(errPrBoxArr):
        IPrange = IPranges[i]
        htmlErrArr[str(IPrange)] = str(elem)
        i += 1

    return jsonp(callback, dict(htmlErrArr))


@route('/status')
def status():
    return {'status': 'online', 'servertime': time.time()}


def getCurretTime():
    timeNow = time.time()
    datetimeUnix = str((int(timeNow)+120)/300*300)  # round to strict 5 min interval
    return str(int(datetimeUnix) - 300)  # search the previous 5 min interval


def jsonp(request, dictionary):
    return "%s(%s)" % (request, dictionary)
    return dictionary

run(host='88.83.68.98', port=5124, reloader=True)
