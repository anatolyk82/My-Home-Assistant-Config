#!/bin/bash

MQTT_BROKER="192.168.1.2"

json='{"state":"on","color":{"r":255,"g":"0,"b":0},"transition_name":"Unfold","transition":120,"brightness":255}'

mosquitto_pub -h $MQTT_BROKER -t "light_0fe4e0/channel2/set" -m $json
mosquitto_pub -h $MQTT_BROKER -t "light_0fe4e0/channel3/set" -m $json
