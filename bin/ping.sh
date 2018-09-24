#!/bin/bash

PACKETS=$1
HOST=$2

pingres=`ping -c $PACKETS $HOST | tail -n 2`

transmitted=`echo $pingres | awk '{ print $1 }'`
received=`echo $pingres | awk '{ print $4 }'`
values=`echo $pingres | awk '{ print $14 }'`
time_min=`echo $values | awk -F'/' '{ print $1 }'`
time_avg=`echo $values | awk -F'/' '{ print $2 }'`
time_max=`echo $values | awk -F'/' '{ print $3 }'`

json="{ \"transmitted\":$transmitted, \"received\":$received, \"time_min\":$time_min, \"time_avg\":$time_avg, \"time_max\":$time_max }"
echo $json

