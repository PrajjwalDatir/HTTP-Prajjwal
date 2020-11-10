# RUN CONFIG.PY TO CONFIGURE

import os

'''Max buffer size to accept from a client'''
SIZE = 8192 # 8*1024 = 8MB

'''Gets the Current Working directory (.)'''
ROOT = os.getcwd()

''' 
fav icon which is displayed in title bar of the browser is requested by client
so we define the path of favicon.ico here
'''
favicon = '/images/favicon.ico'
FAVICON = ROOT + favicon # to get absolute path

'''
only HTTP version no. 1.1 is supported for this server.
It depends on the implementation of the dev but I am only supporting 1.1
''' 
RUNNING_VERSION = '1.1'

'''
Number of Thread Requests handled by the server at one time
'''
MAX_REQUESTS = 100

'''
Maximum URL length supported by the server at the time of establishing new connection
'''
MAX_URL = 150

'''
log file path so that we can write into it
'''
LOG = ROOT + '/server.log'
w = open(LOG, "a") # using a mode so we can only append and not overrite etc bad stuff
w.close()

'''
workfile.html has the response saved msg.
It is not part of the Server program I am using it show client that it's response is saved
'''
WORKFILE = ROOT + '/workfile.html' # path

'''
this creates a basic html workfile
'''
w = open(WORKFILE, "w")
d = '''<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Response Recieved</title>
<body>
    <h1>Yeah We got the response!</h1>
    </br>
    <h1>Your Response was Saved Succesfully!</h1>
</body>
</html>'''
w.write(d)
w.close()

'''
All data entered by the client is stored here for checking Purpose.
'''
CSVFILE = ROOT + '/action_page.csv'
w = open(CSVFILE, "a") # only appending not writing
w.close()

'''
all the files which are deleted using DELETE are getting moved here.
'''
DELETE = ROOT + '/deleted'
'''
the /deleted folder mentioned above is created here.
For the DELETE req purpose
'''
try:
	os.mkdir(DELETE)
except:
	pass

'''
username and password for approval of delete request method
'''
USERNAME = 'maniac' # delete can only be done after checking Auth
PASSWORD = 'datir' # Keep this secret folks


'''
cookie max age 
'''
COOKIE = 'Set-Cookie: id=' # id will be given in the program
MAXAGE = '; max-age=3600' # 3600 sec is 60min

