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
cookie details
'''
COOKIE = 'Set-Cookie: id=' # id will be given in the program
MAXAGE = '; max-age=3600' # 3600 sec is 60min

'''Following is the file formats supported by the server'''
FORMAT = {
		".aac"	: "audio/aac",
		".abw"	: "application/x-abiword",
		".arc"	: "application/x-freearc",
		".avi"	: "video/x-msvideo",
		".azw"	: "application/vnd.amazon.ebook",
		".bin"	: "application/octet-stream",
		".bmp"	: "image/bmp",
		".bz"	: "application/x-bzip",
		".bz2"	: "application/x-bzip2",
		".csh"	: "application/x-csh",
		".css"	: "text/css",
		".csv"	: "text/csv",
		".doc"	: "application/msword",
		".docx"	: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
		".eot"	: "application/vnd.ms-fontobject",
		".epub" : "application/epub+zip",
		".gz"	: "application/gzip",
		".gif"	: "image/gif",
		".htm"	: "text/html",
		".html" : "text/html",
		".ico" 	: "image/vnd.microsoft.icon",
		".ics"	: "text/calendar",
		".jar"	: "application/java-archive",
		".jpeg"	: "image/jpeg",
		".jpg"	: "image/jpeg",
		".js"	: "text/javascript",
		".json"	: "application/json",
		".jsonld": "application/ld+json",
		".mid"	: "audio/midi",
		" .midi": "audio/midi",
		".mjs"	: "text/javascript",
		".mp3"	: "audio.mpeg",
		".mpeg"	: "video/mpeg",
		".mpkg"	: "application/vnd.apple.installer+xml",
		".odp"	: "application/vnd.oasis.opendocument.presentation",
		".ods"	: "application/vnd.oasis.opendocument.spreadsheet",
		".oga"	: "audio/ogg",
		".ogv"	: "video/ogg",
		".ogx"	: "application/ogg",
		".otf"	: "font/otf",
		".png"	: "image/png",
		".pdf"	: "application/pdf",
		".php"	: "appliction/php",
		".ppt"	: "application/vnd.ms-powerpoint",
		".pptx"	: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
		".rar"	: "application/x-rar-compressed",
		".rtf"	: "application/rtf",
		".sh"	: "application/x-sh",
		".svg"	: "image/svg+xml",
		".swf"	: "application/x-shockwave-flash",
		".tar"	: "application/x-tar",
		".tif"	: "image/tiff",
		" .tiff": "image/tiff",
		".ts"	: "video/mp2t",
		".ttf"	: "font/ttf",
		".txt" 	: "text/html",
		".vsd"	: "application/vnd.visio",
		".wav"	: "audio/wav",
		".weba"	: "audio/webm",
		".webm"	: "video/webm",
		".webp"	: ".webp",
		".woff" : "font/woff",
		".woff2": "font/woff2",
		".xhtml": "application/xhtml+xml",
		".xls"	: "application/vnd.ms-excel",
		".xlsx"	: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
		".xml"	: "application/xml",
		".xul"	: "application/vnd.mozilla.xul+xml",
		".zip"	: "application/zip",
		".3gp"	: "video/3gpp",
		".3g2"	: "video/3gpp2",
		".7z"	: "application/x-7z-compressed",
	}

'''Response status codes'''
status_codes = {
		200 : "Ok",
		201	: "Created",
		202	: "Accepted",
		204 : "No Content",
		304 : "Not Modified",
		400 : "Bad Request",
		401 : "Unauthorized",
		403 : "Forbidden",
		404 : "Not Found",
		411 : "Length required",
		412 : "Precondition Failed",
		414 : "URI too long",
		415 : "Unsupported media Type",
		501 : "Not Implemented",
		505 : "HTTP version not supported",
	}

'''Methods supported by the server'''
methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "TRACE", "OPTIONS"]
