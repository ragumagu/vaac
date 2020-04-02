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

# loop through all open windows (ids)
string="["
for win_id in $( wmctrl -l | cut -d' ' -f1 ); do 

    # test if window is a normal window
    if  $( xprop -id $win_id _NET_WM_WINDOW_TYPE | grep -q _NET_WM_WINDOW_TYPE_NORMAL ) ; then 
        appname=$( xprop -id $win_id WM_CLASS | cut -d" " -f4- )
        appname=${appname#?}
        appname=${appname%?}
        string+="{\"key\":\"$appname\",\"value\":\"$win_id\"},"

    fi    
done
string=${string%?}
string+=]
echo $string