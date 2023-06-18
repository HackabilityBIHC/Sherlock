#!/bin/bash
bluetooth="connected"
while true; do
    #check if any device is connected
    connected=$(bluetoothctl devices | cut -f2 -d" " | while read uuid; do bluetoothctl info $uuid; done|grep "Connected: yes")
    
    #device was disconnected
    if [ "$bluetooth" = "disconnected" ]; then
        if [ "$connected" != "" ]; then #found a device connected
            echo "killing sherlock"
            pkill -f "main.py" #kill sherlock process
            bluetooth="connected"
        fi
    fi
    
    #device was connected
    if [ "$bluetooth" = "connected" ]; then
        if [ "$connected" = "" ]; then # no connected device found
            echo "starting sherlock"
            python3 /home/pi/Desktop/Sherlock-dev/src/main.py & #start sherlock (in background)
            bluetooth="disconnected"
        fi
    fi
    sleep 1
done