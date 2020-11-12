#!/bin/bash
################################################################################
while true
do
echo "s to start, q to exit, r to start/ restart."

read key

if [[ "$key" == 'r' ]]
then
    kill $(lsof -t -i:5561)
    gnome-terminal -e "zsh -c \"python3 httpServer.py 5561; exec zsh\""       
elif [[ "$key" == 'q' ]]
then
    echo "Shutting Down... zzzz..."
	# program to quit
    # fuser -k 5561/tcp
    kill $(lsof -t -i:5561)
    # killall terminal
    exit;
elif [[ $key == 's' ]]
then
    echo "Starting :D"
    # killall zsh
    # kill $(lsof -t -i:5561)
    gnome-terminal -e "zsh -c \"python3 httpServer.py 5561; exec zsh\""       
    
else
    echo
fi

done
