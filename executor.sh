#!/bin/bash
if [ "$3" ]; then
	wmctrl -R $3
fi
xdotool $1 $2
