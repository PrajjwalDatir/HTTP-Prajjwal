#!/bin/bash
################################################################################
while true
do
read key
if [[ "$key" == 's' || "$key" == 'r' ]]
then
    gnome-terminal -e "zsh -c \"python3 httpServer.py 5561; exec zsh\""       
    echo "press q to exit, r to restart."
elif [[ "$key" == 'q' ]]
then
    echo "Shutting Down... zzzz..."
	# program to quit
    # fuser -k 5561/tcp
    kill $(lsof -t -i:5561)
    exit;
    exit;
elif [[ $key == 'r' ]]
then
    echo "Restarting :D"
    # killall zsh
    kill $(lsof -t -i:5561)
    exit;
    exit;
else
    echo
fi

done
