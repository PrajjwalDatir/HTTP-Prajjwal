import random
import threading
from socket import *
import os
import shutil				 # to implement delete method
import time
from urllib.parse import *	 # for parsing URL/URI
from _thread import *
import datetime
import mimetypes			 # for getting extensions as well as content types
import base64				 # used for decoding autherization header in delete method
from config import *         # import variables
import sys
import logging
import csv					 # used in put and post method to insert data
import signal                # signal to handle Ctrl+C and other SIGNALS


class methods:
        
    def response_post(self,ent_body, connectionsocket, switcher, glob):
        ip, serverport,scode = glob
        show_response = ''
        query = parse_qs(ent_body)
        entity = CSVFILE
        if os.access(entity, os.W_OK):
            pass
        else:
            status(connectionsocket, 403)
        fields = []
        row = []
        for d in query:
            fields.append(d)
            for i in query[d]:
                row.append(i)
        check = os.path.exists(entity)
        if check:
            fi = open(entity, "a")
            show_response += '\r\nHTTP/1.1 200 OK'
            scode = 200
            csvwriter = csv.writer(fi)
            csvwriter.writerow(row)
        else:
            fi = open(entity, "w")
            show_response += '\r\nHTTP/1.1 201 Created'
            scode = 201
            show_response += '\r\nLocation: ' + entity
            csvwriter = csv.writer(fi)
            csvwriter.writerow(fields)
            csvwriter.writerow(row)
        fi.close()
        show_response += '\r\nServer: ' + ip
        show_response += date()
        f = open(WORKFILE, "rb")
        show_response += '\r\nContent-Language: en-US,en'
        size = os.path.getsize(WORKFILE)
        string = 'Content-Length: ' + str(size)
        show_response += '\r\nContent-Type: text/html'
        show_response += '\r\n' + string
        show_response += '\r\n' + last_modified(entity)
        show_response += '\r\n'
        encoded = show_response.encode()
        connectionsocket.send(encoded)
        connectionsocket.sendfile(f)

    def response_get_head(self,connectionsocket, entity, switcher, query, method, glob):
        serversocket, file_extension, conditional_get, conn, ip, serverport, scode, IDENTITY = glob
        isfile = os.path.isfile(entity)
        isdir = os.path.isdir(entity)
        show_response = ''
        if isfile:
            if (os.access(entity, os.R_OK)):
                if (os.access(entity, os.W_OK)):
                    pass
                else:
                    status(connectionsocket, 403)
            else:
                status(connectionsocket, 403)
            show_response += 'HTTP/1.1 200 OK'
            scode = 200
            try:
                f = open(entity, "rb")
                size = os.path.getsize(entity)
                data = f.read(size)
            except:
                status(connectionsocket, 500)
        elif isdir:
            if os.access(entity, os.R_OK):
                if (os.access(entity, os.W_OK)):
                    pass
                else:
                    status(connectionsocket, 403)
            else:
                status(connectionsocket, 403)
            show_response += 'HTTP/1.1 200 OK'
            scode = 200
            dir_list = os.listdir(entity)
            for i in dir_list:
                if i.startswith('.'):
                    dir_list.remove(i)
        else:
            entity = entity.rstrip('/')
            isdir = os.path.isdir(entity)
            isfile = os.path.isfile(entity)
            if isfile:
                if (os.access(entity, os.R_OK)):
                    if (os.access(entity, os.W_OK)):
                        pass
                else:
                    status(connectionsocket, 403)
                show_response += 'HTTP/1.1 200 OK'
                scode = 200
                try:
                    f = open(entity, "rb")
                    size = os.path.getsize(entity)
                    data = f.read(size)
                except:
                    status(connectionsocket, 500)
            elif isdir:
                if (os.access(entity, os.W_OK) and os.access(entity, os.R_OK)):
                    pass
                else:
                    status(connectionsocket, 403)
                show_response += 'HTTP/1.1 200 OK'
                scode = 200
                dir_list = os.listdir(entity)
                for i in dir_list:
                    if i.startswith('.'):
                        dir_list.remove(i)
            else:	
                status(connectionsocket, 404)
        show_response += '\r\n' + COOKIE + str(IDENTITY) + MAXAGE
        IDENTITY += 1
        for state in switcher:
            if state == 'Host':
                pass
            elif state == 'User-Agent':
                if isfile:
                    show_response += '\r\nServer: ' + ip
                    l = time.ctime().split(' ')
                    l[0] = l[0] + ','
                    string = (' ').join(l)
                    string = 'Date: ' + string
                    show_response += '\r\n' + string
                    show_response += '\r\n' + last_modified(entity)
                elif isdir:
                    show_response += '\r\nServer: ' + ip
            elif state == 'Accept':
                if isdir:
                    string = '\r\nContent-Type: text/html'
                    show_response += string
                elif isfile:
                    try:
                        file_ext = os.path.splitext(entity)
                        if file_ext[1] in file_extension.keys():
                            string = file_extension[file_ext[1]]
                        else:
                            string = 'text/plain'
                        string = '\r\nContent-Type: '+ string
                        show_response += string
                    except:
                        status(connectionsocket, 415)
            elif state == 'Accept-Language':
                if isfile:
                    string = '\r\nContent-Language: ' + switcher[state]
                    show_response += string
                elif isdir:
                    string = '\r\nContent-Language: ' + switcher[state]
                    show_response += string
            elif state == 'Accept-Encoding':
                if isfile:
                    string = '\r\nContent-Length: ' + str(size)
                    show_response += string
            elif state == 'Connection':
                if isfile:
                    conn = 	True
                    show_response += '\r\nConnection: keep-alive'
                elif isdir:
                    conn = False
                    show_response += '\r\nConnection: close'
            elif state == 'If-Modified-Since':
                if_modify(switcher[state], entity)
            else:
                continue
        if isdir and method == 'GET':
            show_response += '\r\n'
            show_response += '\r\n<!DOCTYPE html>'
            show_response += '\r\n<html>\n<head>'
            show_response += '\r\n<title>Directory listing</title>'
            show_response += '\r\n<meta http-equiv="Content-type" content="text/html;charset=UTF-8" /></head>'
            show_response += '\r\n<body><h1>Directory listing..</h1><ul>'
            for line in dir_list:
                if entity == '/':
                    link = 'http://' + ip + ':' + str(serverport) + entity + line
                    l = '\r\n<li><a href ="'+link+'">'+line+'</a></li>'
                    show_response += l
                else:
                    link = 'http://' + ip + ':' + str(serverport) + entity + '/'+ line
                    l = '\r\n<li><a href ="'+link+'">'+line+'</a></li>'
                    show_response += l
            show_response += '\r\n</ul></body></html>'
            encoded = show_response.encode()
            connectionsocket.send(encoded)
            connectionsocket.close()
        elif len(query) > 0 and not isdir and not isfile:
            show_response = []
            entity = CSVFILE
            fields = []
            row = []
            for d in query:
                fields.append(d)
                for i in query[d]:
                    row.append(i)
            check = os.path.exists(entity)
            if check:
                fi = open(entity, "a")
                show_response.append('HTTP/1.1 200 OK')
                scode = 200
                csvwriter = csv.writer(fi)
                csvwriter.writerow(row)
            else:
                fi = open(entity, "w")
                show_response.append('HTTP/1.1 201 Created')
                scode = 201
                show_response.append('Location: ' + entity)
                csvwriter = csv.writer(fi)
                csvwriter.writerow(fields)
                csvwriter.writerow(row)
            fi.close()
            show_response.append('Server: ' + ip)
            show_response.append(date())
            f = open(WORKFILE, "rb")
            show_response.append('Content-Language: en-US,en')
            size = os.path.getsize(WORKFILE)
            string = 'Content-Length: ' + str(size)
            show_response.append('Content-Type: text/html')
            show_response.append(string)
            show_response.append(last_modified(entity))
            show_response.append('\r\n')
            encoded = '\r\n'.join(show_response).encode()
            connectionsocket.send(encoded)
            connectionsocket.sendfile(f)
        elif isfile:
            show_response += '\r\n'
            if conditional_get == False and method == 'GET':
                encoded = show_response.encode()
                connectionsocket.send(encoded)
                connectionsocket.sendfile(f)
            elif conditional_get == False and method == 'HEAD':
                encoded = show_response.encode()
                connectionsocket.send(encoded)
            elif conditional_get == True and (method == 'GET' or method == 'HEAD'):
                status_304(connectionsocket, entity)
        else:
            status(connectionsocket, 400)

    def response_put(self,connectionsocket, addr, ent_body, filedata, entity, switcher, f_flag, scode):
        show_response = []
        isfile = os.path.isfile(entity)
        isdir = os.path.isdir(entity)
        try:
            length = int(switcher['Content-Length'])
        except KeyError:
            status(connectionsocket, 411)
        q = int(length // SIZE)
        r = length % SIZE
        try:
            filedata = filedata + ent_body
        except TypeError:
            ent_body = ent_body.encode()
            filedata = filedata + ent_body
        i = len(ent_body)
        size = length - i
        while size > 0:
            ent_body = connectionsocket.recv(SIZE)
            try:
                filedata = filedata + ent_body
            except TypeError:
                ent_body = ent_body.encode()
                filedata = filedata + ent_body
            size = size - len(ent_body)
        move_p, mode_f, r_201 = False, True, False
        isfile = os.path.isfile(entity)
        isdir = os.path.isdir(entity)
        l = len(entity)
        limit = len(ROOT)
        if l >= limit:
            if isdir:
                if os.access(entity, os.W_OK):
                    pass
                else:
                    status(connectionsocket, 403)
                move_p = True
                loc = ROOT + '/' + str(addr[1])
                try:
                    loc = loc + file_type[switcher['Content-Type'].split(';')[0]]
                except:
                    status(connectionsocket, 403)
                if f_flag == 0:	
                    f = open(loc, "w")
                    f.write(filedata.decode())
                else:
                    f = open(loc, "wb")
                    f.write(filedata)
                f.close()
            elif isfile:
                if os.access(entity, os.W_OK):
                    pass
                else:
                    status(connectionsocket, 403)
                mode_f = True
                if f_flag == 0:	
                    f = open(entity, "w")
                    f.write(filedata.decode())
                else:
                    f = open(entity, "wb")
                    f.write(filedata)
                f.close()
            else:
                #r = random.randint(0,4)
                if ROOT in entity:
                    r_201 = True
                    entity = ROOT + '/' + str(addr[1])
                    try:
                        entity = entity + file_type[switcher['Content-Type'].split(';')[0]]
                    except:
                        status(connectionsocket, 403)
                    if f_flag == 0:	
                        f = open(entity, "w")
                        f.write(filedata.decode())
                    else:
                        f = open(entity, "wb")
                        f.write(filedata)
                    f.close()
                else:
                    mode_f = False
        else:
            move_p = True
            loc = ROOT + '/' + str(addr[1])
            try:
                loc = loc + file_type[switcher['Content-Type']]
            except:
                status(connectionsocket, 403)
            if f_flag == 0:	
                f = open(loc, "w")
            else:
                f = open(loc, "wb")
            f.write(filedata)
            f.close()
        if move_p:
            scode = 301
            show_response.append('HTTP/1.1 301 Moved Permanently')
            show_response.append('Location: ' + loc)
        elif mode_f:
            scode = 204
            show_response.append('HTTP/1.1 204 No Content')
            show_response.append('Content-Location: ' + entity)
        elif r_201:
            scode = 201
            show_response.append('HTTP/1.1 201 Created')
            show_response.append('Content-Location: ' + entity)
        elif not mode_f:
            scode = 501
            show_response.append('HTTP/1.1 501 Not Implemented')
        show_response.append('Connection: keep-alive')
        show_response.append('\r\n')
        return show_response

    def response_delete(self,entity, connectionsocket, ent_body, switcher, glob):
        ip, serverport,scode = glob
        show_response = []
        option_list = entity.split('/')
        isfile = os.path.isfile(entity)
        isdir = os.path.isdir(entity)
        if 'Authorization' in switcher.keys():
            string = switcher['Authorization']
            string = string.split(' ')
            string = base64.decodebytes(string[1].encode()).decode()
            string = string.split(':')
            if string[0] == USERNAME and string[1] == PASSWORD:
                pass
            else:
                scode = 401
                show_response.append('HTTP/1.1 401 Unauthorized')
                show_response.append('WWW-Authenticate: Basic')
                show_response.append('\r\n')
                encoded = '\r\n'.join(show_response).encode()
                connectionsocket.send(encoded)
                return
        else:
            scode = 401
            show_response.append('HTTP/1.1 401 Unauthorized')
            show_response.append('WWW-Authenticate: Basic')
            show_response.append('\r\n')
            encoded = '\r\n'.join(show_response).encode()
            connectionsocket.send(encoded)
            return
        if len(ent_body) > 1 or 'delete' in option_list or isdir:
            scode = 405
            show_response.append('HTTP/1.1 405 Method Not Allowed')
            show_response.append('Allow: OPTIONS, GET, HEAD, POST, PUT')
        elif isfile:
            a = random.randint(0,1)
            if a == 0:
                scode = 200
                show_response.append('HTTP/1.1 200 OK')
            else:
                scode = 204
                show_response.append('HTTP/1.1 204 No Content')
            try:
                if (os.access(entity, os.W_OK) and os.access(entity, os.R_OK)):
                    pass
                else:
                    status(connectionsocket, 403)
                shutil.move(entity, DELETE)
            except shutil.Error:
                os.remove(entity)
        else:
            scode = 400
            show_response.append('HTTP/1.1 400 Bad Request')
        show_response.append('Server: ' + ip)
        show_response.append('Connection: keep-alive')
        show_response.append(date())
        show_response.append('\r\n')
        encoded = '\r\n'.join(show_response).encode()
        connectionsocket.send(encoded)

m = methods()

# function to fetch last modified date of the resource
def last_modified(entity):
    l = time.ctime(os.path.getmtime(entity)).split(' ')
    for i in l:
        if len(i) == 0:
            l.remove(i)
    l[0] = l[0] + ','
    string = (' ').join(l)
    string = 'Last-Modified: ' + string
    return string

#function to check if the resource has been modified or not since the date in HTTP request 
def if_modify(state, entity):
    global conditional_get
    day = state.split(' ')
    if len(day) == 5:
        global month
        m = month[day[1]]
        date = int(day[2])
        t = day[3].split(':')
        t[0], t[1], t[2] = int(t[0]), int(t[1]), int(t[2])
        y = int(day[4])
        ti = datetime.datetime(y, m, date, t[0], t[1], t[2])
        hsec = int(time.mktime(ti.timetuple()))
        fsec = int(os.path.getmtime(entity))
        if hsec == fsec:
            conditional_get = True
        elif hsec < fsec:
            conditional_get = False

#function to return current date
def date():
    l = time.ctime().split(' ')
    l[0] = l[0] + ','
    string = (' ').join(l)
    string = 'Date: ' + string
    return string

#function to give response if server is busy
def status(connectionsocket, code):
    global ip, client_thread, scode
    scode = code
    show_response = []
    if code == 505:
        show_response.append(f'HTTP/1.1 505 {status_codes[505]}')
    elif code == 415:
        show_response.append('HTTP/1.1 415 Unsupported Media Type')
    elif code == 403:
        show_response.append('HTTP/1.1 403 Forbidden')
    elif code == 404:
        show_response.append(f'HTTP/1.1 404 {status_codes[404]}')
    elif code == 414:
        show_response.append('HTTP/1.1 414 Request-URI Too Long')
    elif code == 500:
        show_response.append('HTTP/1.1 500 Internal Server Error')
    elif code == 503:
        show_response.append('HTTP/1.1 503 Server Unavailable')
    show_response.append('Server: ' + ip)
    show_response.append(date())
    show_response.append('\r\n')
    if code == 505:
        show_response.append('Supported Version - HTTP/1.1 \n Rest Unsupported')
    encoded = '\r\n'.join(show_response).encode()
    connectionsocket.send(encoded)
    logging.info('	{}	{}\n'.format(connectionsocket, scode))
    try:
        client_thread.remove(connectionsocket)
        connectionsocket.close()
    except:
        pass
    server()


#function for conditional get implementation
def status_304(connectionsocket, entity):
    global ip
    scode = 304
    show_response = []
    show_response.append('HTTP/1.1 304 Not Modified')
    show_response.append(date())
    show_response.append(last_modified(entity))
    show_response.append('Server: ' + ip)
    show_response.append('\r\n')
    encoded = '\r\n'.join(show_response).encode()
    connectionsocket.send(encoded)

#To breakdown url in request message
def breakdown(entity):
    u = urlparse(entity)
    entity = unquote(u.path)
    if entity == '/':
        entity = os.getcwd()
    query = parse_qs(u.query)
    return (entity, query)


#function which operates between response and requests
def bridgeFunction(connectionsocket, addr, start):
    global serversocket, file_extension, conditional_get, conn, SIZE, client_thread, scode, ip, IDENTITY
    conditional_get = False
    f_flag = 0
    filedata = b""
    conn = True
    urlflag = 0
    while conn :
        message = connectionsocket.recv(SIZE)
        try:
            message = message.decode('utf-8')
            req_list = message.split('\r\n\r\n')
            # print req_list to see it
            # print(req_list)
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
        show_response = []
        header_list = req_list[0].split('\r\n')
        header_len = len(header_list)
        ent_body = req_list[1]
        request_line = header_list[0].split(' ')
        method = request_line[0]
        entity = request_line[1]
        if entity == favicon:
            entity = FAVICON
        elif entity == '/':
            entity = os.getcwd()
        entity, query = breakdown(entity)
        if (len(entity) > MAX_URL and urlflag == 0):
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
            # connectionsocket, entity, switcher, query, method, glob
            m.response_get_head(connectionsocket, entity, switcher, query, method, 
            [serversocket, file_extension, conditional_get, conn, ip, serverport, scode, IDENTITY])
        elif method == 'POST':
            m.response_post(ent_body, connectionsocket, switcher, [ip,serverport, scode])
        elif method == 'PUT':
            show_response = m.response_put(connectionsocket, addr, ent_body, filedata, entity, switcher, f_flag, scode)
            encoded = '\r\n'.join(show_response).encode()
            connectionsocket.send(encoded)
        elif method == 'DELETE':
            m.response_delete(entity, connectionsocket, ent_body, switcher, [ip,serverport, scode])
            conn = False
            connectionsocket.close()
        else:
            method = ''
            break
        # use the logging formatting
        logging.info('	{}	{}	{}	{}	{}\n'.format(addr[0], addr[1], request_line, entity, scode))
    try:
        connectionsocket.close()
        client_thread.remove(connectionsocket)
    except:
        pass

#function handling multiple requests
def server():
    global client_thread
    while True:
        start = 0
        connectionsocket, addr = serversocket.accept() # connectionsocket = request, addr = port,ip

        client_thread.append(connectionsocket)  # add connections
        if(len(client_thread) < MAX_REQUEST):
            start_new_thread(bridgeFunction, (connectionsocket, addr, start))
        else:
            status(connectionsocket, 503)
            connectionsocket.close()
    serversocket.close()

'''
Function to handle the exit ( Ctrl+C and other signals )
'''
sig_rec = False
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    print("q for quit\n r for restart")
    sys.exit(0)


IDENTITY = 0                 # Cookie ID . This project Increments it by 1   

ip = None                    # IP 
file_extension = FORMAT      # Dictionary to convert file extentions into the content types eg. .html to text/html
file_type = FORMAT2          # Dictionary to convert content types into the file extentions eg. text/html to .html

scode = 0                    # Status code initialization
conditional_get = False    	 # check : is it conditional get method?
conn = True					 # to receive requests continuously in client's thread
client_thread = []		     # list to work with the threads
month = MONTH

serversocket = socket(AF_INET, SOCK_STREAM)
s = socket(AF_INET, SOCK_DGRAM)
logging.basicConfig(filename = LOG, level = logging.INFO, format = '%(asctime)s:%(filename)s:%(message)s')


if __name__ == '__main__':
    # To run it on the localhost if you dont want google DNS
    ip = '127.0.0.1'
    # print(ip)
    try:
        serverport = int(sys.argv[1])
    except:
        print("Port Number missing\n\nTO RUN\nType: python3 httpserver.py port_number")
        sys.exit()
    try:
        serversocket.bind(('', serverport))
    except:
        print('\nTO RUN:python3 httpserver.py port_number')
        sys.exit()
    serversocket.listen(5)
    print('HTTP server running on ip: ' + ip + ' port: ' + str(serverport) + '\nGo to this in the browser: (http://' + ip + ':' + str(serverport) + '/)')
    server()            # IMP calling the main server Function
    sys.exit()