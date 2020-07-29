#!/bin/bash

string="(["
for win_id in $( wmctrl -l | cut -d' ' -f1 ); do
    # test if window is a normal window
    if  $( xprop -id $win_id _NET_WM_WINDOW_TYPE | grep -q _NET_WM_WINDOW_TYPE_NORMAL ) ; then
        #appname=$( xprop -id $win_id WM_CLASS | cut -d" " -f4- )
        appname=$( xprop -id $win_id WM_CLASS | awk -F '"' '{print $4F}' )
        #appname=${appname#?}
        #appname=${appname%?}
        string+="{\"key\":\"$appname\",\"value\":\"$win_id\"},"
    fi
done

string=${string%?}
string+='])'
echo $string