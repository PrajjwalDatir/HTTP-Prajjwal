#!/bin/zsh
################################################################################
while true;
do
gnome-terminal -e "zsh -c \"python3 httpServer.py 5561; exec zsh\""       
echo "press q to exit, r to restart."
read $key
if [[ $key == 'q\n' ]];
then
    echo "Shutting Down... zzzz..."
	# program to quit
    # fuser -k 5561/tcp
    kill $(lsof -t -i:5561)
    exit;
else if [[ $key == 'r\n' ]]
    echo "Restarting :D"
    # killall zsh
    kill $p
fi
done