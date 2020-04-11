#!/bin/bash
key="key"
type="type"
if [ "$1" == "$key" ]; then	
	IFS=' '
	read -ra ADDR <<< "$2"
	for i in "${ADDR[@]}"; do
		xdotool key $i
		#echo "Executor.sh: Sending keys" $i
	done
elif [ "$1" == "$type" ]; then	
	xdotool type $2
fi