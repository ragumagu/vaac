#!/bin/bash
key="key"
type="type"
if [ "$1" == "$key" ]; then	
	xdotool key $2	
elif [ "$1" == "$type" ]; then	
	xdotool type $2
fi