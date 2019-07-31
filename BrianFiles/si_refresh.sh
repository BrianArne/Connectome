#!bin/bash

#TODO: 1. change to not require xdotool (open-source toolkit to emulate user
#input through x11), so it does not need to be bundled with ConnectomeProject.
#can do this through figuring out user's window system server (ex. X, Wayland
#Mir, etc.) and running the appropriate commands.
#2. this script itself is made for bash, so must either: a. write using
#commands shared between all unix shells/cmd languages -OR- b. make separate
#scripts and have appropriate one figured out either before python subprocess
#call or python subprocess calls a wrapper script (could also have this
#figured out early and stored in string var, subprocess() call uses var
#in script call, e.g. "subprocess.call([var, ..., ...])")


SIPID="$1"
#echo $SIPID

ORIGWINID=`xdotool getactivewindow`
#echo $ORIGWINID

SIWINID=`xdotool search --pid=$SIPID --name --all "Surf Ice"`
#echo $SIWINID

xdotool windowactivate --sync $SIWINID key ctrl+r
xdotool windowactivate --sync $ORIGWINID
