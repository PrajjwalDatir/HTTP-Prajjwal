from socket import *         # to implement webserver
from datetime import *		 # to implement conditional get
import os					 # to use basic facilities of checking path,file, directory
import time					 # to implement conditional get
import random				 # to implement randomness so that some of the status codes get implemented
import threading			 # to handle requests coming to server
from urllib.parse import *	 # for parsing URL/URI
from _thread import *
import shutil				 # to implement delete method
import mimetypes			 # for getting extensions as well as content types
import csv					 # used in get and post method to insert the data into file
import base64				 # used for decoding autherization header in delete method
import sys					 # for arguements, exits
import logging				 # for logging
from config import *         # import some variable values
import signal                # signal to handle Ctrl+C and other SIGNALS

serversocket = socket(AF_INET, SOCK_STREAM)
s = socket(AF_INET, SOCK_DGRAM)
logging.basicConfig(filename = LOG, level = logging.INFO, format = '%(asctime)s:%(filename)s:%(message)s')

lthread = []				 # list to work with the threads
file_extension = FORMAT      # Dictionary to convert file extentions into the content types eg. .html to text/html
file_type = FORMAT2          # Dictionary to convert content types into the file extentions eg. text/html to .html
month = MONTH

ip = '0.0.0.0'               # IP 

scode = 0                    # Status code initialization
conditional_get = False    	 # check : is it conditional get method?
conn = True					 # to receive requests continuously in client's thread

#function to implement post method 		
def method_post(ent_body, connectionsocket, switcher):
    global ip, scode
    display = []
    query = parse_qs(ent_body)
    element = CSVFILE
    if os.access(element, os.W_OK):
        pass
    else:
        status(connectionsocket, 403)
    fields = []
    row = []
    for d in query:
        fields.append(d)
        for i in query[d]:
            row.append(i)
    check = os.path.exists(element)
    if check:
        fi = open(element, "a")
        display.append('HTTP/1.1 200 OK')
        scode = 200
        csvwriter = csv.writer(fi)
        csvwriter.writerow(row)
    else:
        fi = open(element, "w")
        display.append('HTTP/1.1 201 Created')
        scode = 201
        display.append('Location: ' + element)
        csvwriter = csv.writer(fi)
        csvwriter.writerow(fields)
        csvwriter.writerow(row)
    fi.close()
    display.append('Server: ' + ip)
    display.append(date())
    f = open(WORKFILE, "rb")
    display.append('Content-Language: en-US,en')
    size = os.path.getsize(WORKFILE)
    string = 'Content-Length: ' + str(size)
    display.append('Content-Type: text/html')
    display.append(string)
    display.append(last_modified(element))
    display.append('\r\n')
    encoded = '\r\n'.join(display).encode()
    connectionsocket.send(encoded)
    connectionsocket.sendfile(f)

#function to implement delete method
def method_delete(element, connectionsocket, ent_body, switcher):
    global ip, scode
    display = []
    option_list = element.split('/')
    isfile = os.path.isfile(element)
    isdir = os.path.isdir(element)
    if 'Authorization' in switcher.keys():
        string = switcher['Authorization']
        string = string.split(' ')
        string = base64.decodebytes(string[1].encode()).decode()
        string = string.split(':')
        if string[0] == USERNAME and string[1] == PASSWORD:
            pass
        else:
            scode = 401
            display.append('HTTP/1.1 401 Unauthorized')
            display.append('WWW-Authenticate: Basic')
            display.append('\r\n')
            encoded = '\r\n'.join(display).encode()
            connectionsocket.send(encoded)
            return
    else:
        scode = 401
        display.append('HTTP/1.1 401 Unauthorized')
        display.append('WWW-Authenticate: Basic')
        display.append('\r\n')
        encoded = '\r\n'.join(display).encode()
        connectionsocket.send(encoded)
        return
    if len(ent_body) > 1 or 'delete' in option_list or isdir:
        scode = 405
        display.append('HTTP/1.1 405 Method Not Allowed')
        display.append('Allow: OPTIONS, GET, HEAD, POST, PUT')
    elif isfile:
        a = random.randint(0,1)
        if a == 0:
            scode = 200
            display.append('HTTP/1.1 200 OK')
        else:
            scode = 204
            display.append('HTTP/1.1 204 No Content')
        try:
            if (os.access(element, os.W_OK) and os.access(element, os.R_OK)):
                pass
            else:
                status(connectionsocket, 403)
            shutil.move(element, DELETE)
        except shutil.Error:
            os.remove(element)
    else:
        scode = 400
        display.append('HTTP/1.1 400 Bad Request')
    display.append('Server: ' + ip)
    display.append('Connection: keep-alive')
    display.append(date())
    display.append('\r\n')
    encoded = '\r\n'.join(display).encode()
    connectionsocket.send(encoded)
#function to implement get and head method
def method_get_head(connectionsocket, element, switcher, query, method):
    global serversocket, file_extension, conditional_get, conn, ip, scode, IDENTITY
    isfile = os.path.isfile(element)
    isdir = os.path.isdir(element)
    display = []
    if isfile:
        if (os.access(element, os.W_OK) and os.access(element, os.R_OK)):
            pass
        else:
            status(connectionsocket, 403)
        display.append('HTTP/1.1 200 OK')
        scode = 200
        try:
            f = open(element, "rb")
            size = os.path.getsize(element)
            data = f.read(size)
        except:
            status(connectionsocket, 500)
    elif isdir:
        if (os.access(element, os.W_OK) and os.access(element, os.R_OK)):
            pass
        else:
            status(connectionsocket, 403)
        display.append('HTTP/1.1 200 OK')
        scode = 200
        dir_list = os.listdir(element)
        for i in dir_list:
            if i.startswith('.'):
                dir_list.remove(i)
    else:
        element = element.rstrip('/')
        isfile = os.path.isfile(element)
        isdir = os.path.isdir(element)
        if isfile:
            if (os.access(element, os.W_OK) and os.access(element, os.R_OK)):
                pass
            else:
                status(connectionsocket, 403)
            display.append('HTTP/1.1 200 OK')
            scode = 200
            try:
                f = open(element, "rb")
                size = os.path.getsize(element)
                data = f.read(size)
            except:
                status(connectionsocket, 500)
        elif isdir:
            if (os.access(element, os.W_OK) and os.access(element, os.R_OK)):
                pass
            else:
                status(connectionsocket, 403)
            display.append('HTTP/1.1 200 OK')
            scode = 200
            dir_list = os.listdir(element)
            for i in dir_list:
                if i.startswith('.'):
                    dir_list.remove(i)
        else:	
            status(connectionsocket, 404)
    display.append(COOKIE + str(IDENTITY) + MAXAGE)
    IDENTITY += 1
    for state in switcher:
        if state == 'Host':
            pass
        elif state == 'User-Agent':
            if isfile:
                display.append('Server: ' + ip)
                display.append(date())
                display.append(last_modified(element))
            elif isdir:
                display.append('Server: ' + ip)
        elif state == 'Accept':
            if isdir:
                string = 'Content-Type: text/html'
                display.append(string)
            elif isfile:
                try:
                    file_ext = os.path.splitext(element)
                    if file_ext[1] in file_extension.keys():
                        string = file_extension[file_ext[1]]
                    else:
                        string = 'text/plain'
                    string = 'Content-Type: '+ string
                    display.append(string)
                except:
                    status(connectionsocket, 415)
        elif state == 'Accept-Language':
            if isfile:
                string = 'Content-Language: ' + switcher[state]
                display.append(string)
            elif isdir:
                string = 'Content-Language: ' + switcher[state]
                display.append(string)
        elif state == 'Accept-Encoding':
            if isfile:
                string = 'Content-Length: ' + str(size)
                display.append(string)
        elif state == 'Connection':
            if isfile:
                conn = 	True
                display.append('Connection: keep-alive')
            elif isdir:
                conn = False
                display.append('Connection: close')
        elif state == 'If-Modified-Since':
            if_modify(switcher[state], element)
        elif state == 'Cookie':
            IDENTITY -= 1 
            display.remove(COOKIE + str(IDENTITY) + MAXAGE)
        else:
            continue
    if isdir and method == 'GET':
        display.append('\r\n')
        display.append('<!DOCTYPE html>')
        display.append('<html>\n<head>')
        display.append('<title>Directory listing</title>')
        display.append('<meta http-equiv="Content-type" content="text/html;charset=UTF-8" /></head>')
        display.append('<body><h1>Directory listing..</h1><ul>')
        for line in dir_list:
            if element == '/':
                link = 'http://' + ip + ':' + str(serverport) + element + line
                l = '<li><a href ="'+link+'">'+line+'</a></li>'
                display.append(l)
            else:
                link = 'http://' + ip + ':' + str(serverport) + element + '/'+ line
                l = '<li><a href ="'+link+'">'+line+'</a></li>'
                display.append(l)
        display.append('</ul></body></html>')
        encoded = '\r\n'.join(display).encode()
        connectionsocket.send(encoded)
        connectionsocket.close()
    elif len(query) > 0 and not isdir and not isfile:
        display = []
        element = CSVFILE
        fields = []
        row = []
        for d in query:
            fields.append(d)
            for i in query[d]:
                row.append(i)
        check = os.path.exists(element)
        if check:
            fi = open(element, "a")
            display.append('HTTP/1.1 200 OK')
            scode = 200
            csvwriter = csv.writer(fi)
            csvwriter.writerow(row)
        else:
            fi = open(element, "w")
            display.append('HTTP/1.1 201 Created')
            scode = 201
            display.append('Location: ' + element)
            csvwriter = csv.writer(fi)
            csvwriter.writerow(fields)
            csvwriter.writerow(row)
        fi.close()
        display.append('Server: ' + ip)
        display.append(date())
        f = open(WORKFILE, "rb")
        display.append('Content-Language: en-US,en')
        size = os.path.getsize(WORKFILE)
        string = 'Content-Length: ' + str(size)
        display.append('Content-Type: text/html')
        display.append(string)
        display.append(last_modified(element))
        display.append('\r\n')
        encoded = '\r\n'.join(display).encode()
        connectionsocket.send(encoded)
        connectionsocket.sendfile(f)
    elif isfile:
        display.append('\r\n')
        if conditional_get == False and method == 'GET':
            encoded = '\r\n'.join(display).encode()
            connectionsocket.send(encoded)
            connectionsocket.sendfile(f)
        elif conditional_get == False and method == 'HEAD':
            encoded = '\r\n'.join(display).encode()
            connectionsocket.send(encoded)
        elif conditional_get == True and (method == 'GET' or method == 'HEAD'):
            status_304(connectionsocket, element)
    else:
        status(connectionsocket, 400)

#function which operate on top of the methods i.e bridge between response and requests
def clientfun(connectionsocket, addr, start):
    global serversocket, file_extension, conditional_get, conn, SIZE, lthread, SERVER, MAIN, scode
    conditional_get = False
    f_flag = 0
    filedata = b""
    conn = True
    urlflag = 0
    while conn and SERVER and MAIN:
        message = connectionsocket.recv(SIZE)
        try:
            message = message.decode('utf-8')
            req_list = message.split('\r\n\r\n')
            # print req_list to see it
            print(req_list)
            f_flag = 0
        except UnicodeDecodeError:
            # if you're using non UTF-8 chars
            req_list = message.split(b'\r\n\r\n')
            req_list[0] = req_list[0].decode(errors = 'ignore')
            print(req_list)
            f_flag = 1
        if len(req_list) > 1:
            # every line ends with a \r\n so for only headers it'll create ['req', '']
            pass
        else:
            break
        try:
            log.write(((addr[0]) + '\n' + req_list[0] + '\n\n'))
        except:
            pass
        display = []
        header_list = req_list[0].split('\r\n')
        header_len = len(header_list)
        ent_body = req_list[1]
        request_line = header_list[0].split(' ')
        method = request_line[0]
        element = request_line[1]
        if element == favicon:
            element = FAVICON
        elif element == '/':
            element = os.getcwd()
        element, query = resolve(element)
        if (len(element) > MAX_URL and urlflag == 0):
            status(connectionsocket, 414)
            break
        else:
            urlflag = 1
        version = request_line[2]
        try:
            version_num = version.split('/')[1]
            if not (version_num == RUNNING_VERSION):
                status(connectionsocket, 505)
        except IndexError:
            status(connectionsocket, 505)
        switcher = {}
        request_line = header_list.pop(0)
        for line in header_list :
            line_list = line.split(': ')
            switcher[line_list[0]] = line_list[1]
        if method == 'GET' or method == 'HEAD':
            method_get_head(connectionsocket, element, switcher, query, method)
        elif method == 'POST':
            method_post(ent_body, connectionsocket, switcher)
        elif method == 'PUT':
            display = method_put(connectionsocket, addr, ent_body, filedata, element, switcher, f_flag)
            encoded = '\r\n'.join(display).encode()
            connectionsocket.send(encoded)
        elif method == 'DELETE':
            method_delete(element, connectionsocket, ent_body, switcher)
            conn = False
            connectionsocket.close()
        elif method == 'CONNECT':
            method_connect(connectionsocket, switcher)
            conn = True
        elif method == 'OPTIONS':
            method_option(element, connectionsocket, switcher)
            conn = False
            connectionsocket.close()
        elif method == 'TRACE':
            method_trace(req_list[0], connectionsocket, switcher)
            conn = False
            connectionsocket.close()
        else:
            method = ''
            break
        logging.info('	{}	{}	{}	{}	{}\n'.format(addr[0], addr[1], request_line, element, scode))
    try:
        connectionsocket.close()
        lthread.remove(connectionsocket)
    except:
        pass

#function handling multiple requests
def server():
    global lthread
    while True:
        start = 0
        connectionsocket, addr = serversocket.accept() # connectionsocket = request, addr = port,ip
        # TODO print
        lthread.append(connectionsocket)  # add connections
        if(len(lthread) < MAX_REQUESTS):
            start_new_thread(clientfun, (connectionsocket, addr, start))
        else:
            status(connectionsocket, 503)
            connectionsocket.close()
    serversocket.close()

'''
Function to handle the exit ( Ctrl+C and other signals )
'''
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    print("q for quit\n r for restart")
    sys.exit(0)


''' TO find the server's ip address
Link : https://developers.google.com/speed/public-dns/docs/using
above is the source of 8.8.8.8 ip
'''
def findip():
    try:
        s.connect(('8.8.8.8', 8000))
        IP = s.getsockname()[0]
    except:
        # localhost by default
        IP = '127.0.0.1'
    s.close()
    return IP


if __name__ == '__main__':
    # To run it on the localhost if you dont want google DNS
    try:
        if sys.argv[2] == 'localhost':
            ip = '127.0.0.1'
        else:
            ip = str(findip())
    except:
        pass
    if not ip:
        ip = str(findip())
    # print(ip)
    try:
        serverport = int(sys.argv[1])
    except:
        print("Port Number missing\n\nTO RUN\nType: python3 httpserver.py port_number")
        sys.exit()
    try:
        serversocket.bind(('', serverport))
    except:
        print('HTTPServer invalid arguements')
        print('\nTO RUN\nType: python3 httpserver.py port_number')
        sys.exit()
    serversocket.listen(40)
    print('HTTP server running on ip: ' + ip + ' port: ' + str(serverport) + '\n(http://' + ip + ':' + str(serverport) +'/)')
    server()
    sys.exit()