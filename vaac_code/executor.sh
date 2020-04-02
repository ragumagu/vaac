#!/bin/bash
#echo "In Executor.sh"
#if [ "$3" ]; then
#	#echo "Executor.sh: Focusing" $3
#	#wmctrl -a $3
#	xdotool  search -desktop 0 --onlyvisible --class $3 windowactivate
#fi

key="key"
type="type"
if [ "$1" == "$key" ]; then	
	IFS=' '
	read -ra ADDR <<< "$2"
	for i in "${ADDR[@]}"; do
		xdotool key $i
		echo "Executor.sh: Sending keys" $i
	done
elif [ "$1" == "$type" ]; then	
	xdotool type $2
fi

#echo "Returning from executor.sh"