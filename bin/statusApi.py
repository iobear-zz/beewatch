#!/usr/bin/python
#

from bottle import route, run, request, abort
import redis
import time
import struct
import socket
import re
import string

r_server = redis.Redis(host='localhost', port=6380, db=0)


@route('/v1/stb/ip/:ip', method='GET')
def get_ip(ip):
    ipDec = struct.unpack('>L', socket.inet_aton(ip))[0]  # convert IP to decimal
    mac = r_server.get(ipDec)  # look for IP at redisDB

    if not mac:
        abort(404, 'No stb with ip %s' % ip)

    return "{ mac: %s}" % mac


@route('/v1/stb/mac/:mac', method='GET')
def get_mac(mac):
    REGEXmac = re.compile(r"([\dA-Fa-f])")
    AtoF0to9 = REGEXmac.findall(mac)
    cleanMac = str.upper("".join(AtoF0to9))
    timeSearchString = getCurretTime()
    loop = 0

    while loop < 432000:  # search the last 5 days -- 1 day = 86400 sec * 5
        searchStr = str(int(timeSearchString) - loop) + cleanMac
        result = r_server.hgetall(searchStr)  # look for time+mac at redisDB

        if result:
            break

        loop += 300

    if not result:
        abort(404, 'No stb with mac %s' % cleanMac)

    return result


@route('/status')
def status():
    return {'status': 'online', 'servertime': time.time()}


def getCurretTime():
    timeNow = time.time()
    datetimeUnix = str((int(timeNow)+120)/300*300)  # round to strict 5 min interval
    return str(int(datetimeUnix) - 300)  # search the previous 5 min interval


run(host='88.83.68.98', port=5123, reloader=True)
