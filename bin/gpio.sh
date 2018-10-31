#!/bin/bash

GPIO_PIN=18
LEVEL=0 #or 1

#-------------------

PIN_DIR=/sys/class/gpio/gpio${GPIO_PIN}

if [ ! -f $PIN_DIR ]
then
    # Exports pin to userspace
	echo $GPIO_PIN > /sys/class/gpio/export
	sleep 2	
	
	# Sets pin as an output
	echo "out" > /sys/class/gpio/gpio${GPIO_PIN}/direction
	sleep 1
fi

# Sets pin to high
echo $LEVEL > /sys/class/gpio/gpio${GPIO_PIN}/value

