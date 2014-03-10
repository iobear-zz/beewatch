#!/bin/bash
#
#

TXT=1
MINLOGWORKERS=6

if [ "$1" == "notxt" ]; then
    TXT=""
fi

if [ $TXT ]; then
    echo
    echo "------------------------------"
    echo
fi

PSYSLOG=`ps aux | grep psyslog.py | wc -l`
if [ $PSYSLOG -gt 1 ]; then
    if [ $TXT ]; then
        echo "pSyslog - OK"
    fi
else
    if [ $TXT ]; then
        echo "pSyslog - NOT running - please enter:"
	echo
	echo "sudo /usr/bin/python /home/beeadmin/beewatch/bin/psyslog.py &"
    fi
    #/usr/bin/python /home/beeadmin/beewatch/bin/psyslog.py &
fi

STATUSAPI=`ps aux | grep statusApi.py | wc -l`
if [ $STATUSAPI -gt 1 ]; then
    if [ $TXT ]; then
        echo "statusAPI - OK"
    fi
else
    if [ $TXT ]; then
        echo "statusAPI - NOT running - restarting.."
    fi
    /usr/bin/python /home/beeadmin/beewatch/bin/statusApi.py &

fi

AIRTIESWORKER=`ps aux | grep parse_airties_logs.py | wc -l`
if [ $AIRTIESWORKER -gt $MINLOGWORKERS ]; then
    if [ $TXT ]; then
        echo "logWorkers - OK"
    fi
else
    if [ $TXT ]; then
        echo "logWorkers - NOT all up - starting one more.."
    fi
    /usr/bin/python /home/beeadmin/beewatch/bin/parse_airties_logs.py &

fi

REDISRAW=`ps aux | grep redis.conf | wc -l`
if [ $REDISRAW -gt 1 ]; then
    if [ $TXT ]; then
        echo "redisRaw - OK"
    fi
else
    if [ $TXT ]; then
        echo "redisRaw - NOT running"
    fi
fi

REDISPARSED=`ps aux | grep redis-parsed.conf | wc -l`
if [ $REDISPARSED -gt 1 ]; then
    if [ $TXT ]; then
        echo "redisParsed - OK"
    fi
else
    if [ $TXT ]; then
        echo "redisParsed - NOT running"
    fi
fi

if [ $TXT ]; then
    echo
    echo "------------------------------"
    echo 
fi

