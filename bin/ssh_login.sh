#!/bin/bash

# In /ets/rsyslog.conf the option $FileCreateMode must be 0644

LOGFILE=/var/log/auth.log
LAST_COUNT=/tmp/auth.sensor

sensor_status="ok"
linesToCheck=0
failedAttempts=0
if [ -r $LOGFILE ]
then
	currentAmountOfLines=`/bin/cat $LOGFILE | /usr/bin/wc -l`

	previousAmountOfLines=0
	if [ -f $LAST_COUNT ]
	then
		previousAmountOfLines=`/bin/cat $LAST_COUNT`
	fi

	linesToCheck=$currentAmountOfLines
	if [ $currentAmountOfLines -ge $previousAmountOfLines ]
	then
		linesToCheck=`/usr/bin/expr $currentAmountOfLines - $previousAmountOfLines`
	fi

	echo $currentAmountOfLines > $LAST_COUNT

	failedAttempts=`/usr/bin/tail -n $linesToCheck $LOGFILE | /bin/grep sshd | /bin/grep "Failed password" | wc -l`

	if [ "$failedAttempts" -gt 3 ]
	then
		sensor_status="warning"
	fi
else
	sensor_status="no access"
fi

json="{ \"failed_attempts\":$failedAttempts, \"status\":\"$sensor_status\", \"last_scan\":\"`date +'%Y-%m-%d %H:%M:%S'`\", \"last_scanned_lines\":\"$linesToCheck\" }"
echo $json
