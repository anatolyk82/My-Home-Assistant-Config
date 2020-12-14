#!/bin/bash

MQTT_BROKER="192.168.1.2"

#trap turn_off 2
indx=$((1 + $RANDOM % 20))
indx=`expr $indx - 1`

allEffects=(
'{"state":"on","color":{"r":255,"g:"0,"b":0},"effect":"Chase2Up","parameter1":255,"parameter2":30,"brightness":255}'
'{"state":"on","effect":"BigSparks","parameter1":255,"parameter2":255,"brightness":255}'
'{"state":"on","effect":"SparklesOnColorLoop","parameter1":255,"parameter2":255,"brightness":255}'
'{"state":"on","effect":"ChaseUp","parameter1":240,"parameter2":128,"brightness":255}'
'{"state":"on","effect":"PeriodicMeteorsDown","parameter1":255,"parameter2":255,"brightness":255}'
'{"state":"on","effect":"Starburst","parameter1":255,"parameter2":255,"brightness":255}'
'{"state":"on","effect":"RGBScanner","parameter1":200,"parameter2":100,"brightness":255}'
'{"state":"on","effect":"Pixie","parameter1":0,"parameter2":150,"brightness":255}'
'{"state":"on","color":{"r":255,"g:"0,"b":0},"effect":"Flicker","parameter1":128,"parameter2":200,"brightness":255}'
'{"state":"on","effect":"RandomColor","parameter1":200,"parameter2":200,"brightness":255}'
'{"state":"on","color":{"r":255,"g:"0,"b":0},"effect":"MultiplePixelQueues","parameter1":230,"parameter2":220,"brightness":255}'
'{"state":"on","effect":"Rainbow","parameter1":255,"parameter2":200,"brightness":255}'
'{"state":"on","effect":"FastPixels","parameter1":10,"parameter2":40,"brightness":255}'
'{"state":"on","effect":"RunAndLightUp","parameter1":255,"parameter2":0,"brightness":255}'
'{"state":"on","color":{"r":0,"g:"0,"b":255},"effect":"Flicker","parameter1":255,"parameter2":200,"brightness":255}'
'{"state":"on","color":{"r":0,"g:"0,"b":255},"effect":"MultiplePixelQueues","parameter1":230,"parameter2":220,"brightness":255}'
'{"state":"on","effect":"MultipleColorPixelQueues","parameter1":230,"parameter2":220,"brightness":255}'
'{"state":"on","effect":"EnergySource","parameter1":230,"parameter2":200,"brightness":255}'
'{"state":"on","effect":"EnergyHole","parameter1":230,"parameter2":200,"brightness":255}'
'{"state":"on","effect":"Neutrinos","parameter1":235,"parameter2":255,"brightness":255}'
)

#json=${allEffects[$1]}
json=${allEffects[$indx]}
#echo "Current effect: $json" # > /tmp/julgran_effect.txt
mosquitto_pub -h $MQTT_BROKER -t "light_0fe4e0/channel2/set" -m $json
mosquitto_pub -h $MQTT_BROKER -t "light_0fe4e0/channel3/set" -m $json


