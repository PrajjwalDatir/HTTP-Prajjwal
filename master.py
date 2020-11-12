# Master file to run everything
import os
import sys

while True:
    # TO run the server with port number
    print("Hit 'Ctrl+C' to get menu to quit & Restart the server.")
    print("################################################################################\n################################################################################\n################################################################################\n\n")
    
    print("Starting the server ...")

    # os.system(f'python3 httpServer.py {sys.argv[1]}')
    while True:
        print("q for quit\nr for restart.")
        key = input()
        if key=='q':
            exit()
        elif key=='r':
            print("restarting the server ...")
            break
        else:
            print("invalid input\n")
            continue
exit()