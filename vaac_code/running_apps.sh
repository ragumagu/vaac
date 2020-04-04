#!/bin/bash

#applications=()
#
## loop through all open windows (ids)
#for win_id in $( wmctrl -l | cut -d' ' -f1 ); do 
#
#    # test if window is a normal window
#    if  $( xprop -id $win_id _NET_WM_WINDOW_TYPE | grep -q _NET_WM_WINDOW_TYPE_NORMAL ) ; then 
#
#        # filter application name and remove double-quote at beginning and end
#        appname=$( xprop -id $win_id WM_CLASS | cut -d" " -f4 )
#        appname=${appname#?}
#        appname=${appname%?}
#
#        # add to result list
#        applications+=( "$appname" ) 
#
#    fi
#
#done

# sort result list and remove duplicates  
#readarray -t applications < <(printf '%s\0' "${applications[@]}" | sort -z | xargs -0n1 | uniq)

#printf -- '%s\n' "${applications[@]}"

#The following assignment to x is to overcome a race condition.
#x=$(xdotool search --sync class "gnome-terminal")
#echo "x is",$x

# loop through all open windows (ids)
string="["
for win_id in $( wmctrl -l | cut -d' ' -f1 ); do 
    echo "In running_apps.sh, win_id",$win_id
    # test if window is a normal window
    if  $( xprop -id $win_id _NET_WM_WINDOW_TYPE | grep -q _NET_WM_WINDOW_TYPE_NORMAL ) ; then 
        appname=$( xprop -id $win_id WM_CLASS | cut -d" " -f4- )
        appname=${appname#?}
        appname=${appname%?}
        string+="{\"key\":\"$appname\",\"value\":\"$win_id\"},"

    fi    
done

#root_id=$( xwininfo -root | grep "Window id" | cut -d" " -f4 )
#string+="{\"key\":\"root_window\",\"value\":\"$root_id\"}"
string=${string%?}
string+=]
echo $string