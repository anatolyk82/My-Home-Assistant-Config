#!/bin/bash

MQTT_BROKER="192.168.1.2"

json='{"state":"off","transition_name":"FadeOut","transition":60}'

mosquitto_pub -h $MQTT_BROKER -t "light_0fe4e0/channel2/set" -m $json
mosquitto_pub -h $MQTT_BROKER -t "light_0fe4e0/channel3/set" -m $json

