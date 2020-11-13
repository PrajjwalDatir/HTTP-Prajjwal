from socket import *
from datetime import *
import os
import time
import random
import threading
from _thread import *
import shutil		            		 # to implement delete method
import csv          					 # used in put and post method to insert data
import base64		            		 # used for decoding autherization header in delete method
import sys
import logging
from config import *                    # import variables
import signal                           # signal to handle Ctrl+C and other SIGNALS
from supplement.breakdown import *      # to breakdown entity
from supplement.last_modified import *  # last_modified for condi get

ip = None                    # IP 
conn = True					 # to receive requests continuously in client's thread
scode = 0                    # Status code initialization

IDENTITY = 0                 # Cookie ID . This project Increments it by 1   
conditional_get = False    	 # check : is it conditional get method?
month = MONTH

file_type = FORMAT2          # Dictionary to convert content types into the file extentions eg. text/html to .html
file_extension = FORMAT      # Dictionary to convert file extentions into the content types eg. .html to text/html

client_thread = []		     # list to work with the threads

serversocket = socket(AF_INET, SOCK_STREAM)
s = socket(AF_INET, SOCK_DGRAM)
logging.basicConfig(filename = LOG, level = logging.INFO, format = '%(asctime)s:%(filename)s:%(message)s')


class methods:
        
    def response_post(self,ent_body, connectionsocket, switcher, glob):
        ip, serverport,scode = glob
        show_response = ''
        entity = CSVFILE
        query = parse_qs(ent_body)
        if os.access(entity, os.W_OK):
            pass
        else:
            status(connectionsocket, 403)
        fields = ''
        row = ''
        for d in query:
            fields += d + ', '
            for i in query[d]:
                row += i + ', '
        file_exists = os.path.exists(entity)
        if file_exists:
            fi = open(entity, "a")
            show_response += 'HTTP/1.1 200 OK'
            scode = 200
            csvwriter = csv.writer(fi)
            csvwriter.writerow(row)
        else:
            fi = open(entity, "w")
            show_response += 'HTTP/1.1 201 Created'
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
        conversation = 'Content-Length: ' + str(size)
        show_response += '\r\nContent-Type: text/html'
        show_response += '\r\n' + conversation
        show_response += '\r\n' + last_modified(entity)
        show_response += '\r\n\r\n'
        encoded = show_response.encode()
        connectionsocket.send(encoded)
        connectionsocket.sendfile(f)
        return [ip, serverport, scode]

    def response_get_head(self,connectionsocket, entity, switcher, query, method, glob):
        serversocket, file_extension, conditional_get, conn, ip, serverport, scode, IDENTITY = glob
        isfile = os.path.isfile(entity)
        isdir = os.path.isdir(entity)
        show_response = ''
        if isfile:
            show_response += 'HTTP/1.1 200 OK'
            scode = 200
            if (os.access(entity, os.R_OK)):
                if (os.access(entity, os.W_OK)):
                    pass
                else:
                    status(connectionsocket, 403)
            else:
                status(connectionsocket, 403)
            try:
                f = open(entity, "rb")
                size = os.path.getsize(entity)
                data = f.read(size)
            except:
                status(connectionsocket, 500)
        elif isdir:
            dir_list = os.listdir(entity)
            show_response += 'HTTP/1.1 200 OK'
            scode = 200
            # if it is a directory
            if os.access(entity, os.R_OK):
                if (os.access(entity, os.W_OK)):
                    pass
                else:
                    status(connectionsocket, 403)
            else:
                status(connectionsocket, 403)
            for i in dir_list:
                if i.startswith('.'):
                    dir_list.remove(i)
                else:
                    pass
        else:
            entity = entity.rstrip('/')
            isdir = os.path.isdir(entity)
            isfile = os.path.isfile(entity)
            if isfile:
                show_response += 'HTTP/1.1 200 OK'
                scode = 200
                if (os.access(entity, os.R_OK)):
                    if (os.access(entity, os.W_OK)):
                        pass
                else:
                    status(connectionsocket, 403)
                try:
                    size = os.path.getsize(entity)
                    f = open(entity, "rb")
                    data = f.read(size)
                except:
                    # error while accesing the file
                    status(connectionsocket, 500)
            elif isdir:
                scode = 200
                show_response += 'HTTP/1.1 200 OK'
                dir_list = os.listdir(entity)
                if (os.access(entity, os.W_OK)):
                    if (os.access(entity, os.R_OK)):
                        pass
                    else:
                        status(connectionsocket, 403)
                else:
                    status(connectionsocket, 403)
                for i in dir_list:
                    if i.startswith('.'):
                        dir_list.remove(i)
                    else:
                        pass
            else:	
                status(connectionsocket, 404)
        show_response += '\r\n' + COOKIE + str(IDENTITY) + MAXAGE
        IDENTITY += random.randint(1,10)
        for state in switcher:
            if state == 'User-Agent':
                if isfile:
                    show_response += '\r\nServer: ' + ip
                    l = time.ctime().split(' ')
                    l[0] = l[0] + ','
                    conversation = (' ').join(l)
                    conversation = '\r\nDate: ' + conversation
                    show_response += conversation
                    show_response += '\r\n' + last_modified(entity)
                elif isdir:
                    show_response += '\r\nServer: ' + ip
            elif state == 'Host':
                pass
            elif state == 'Accept':
                if isdir:
                    conversation = '\r\nContent-Type: text/html'
                    show_response += conversation
                elif isfile:
                    try:
                        file_ext = os.path.splitext(entity)
                        if file_ext[1] in file_extension.keys():
                            conversation = file_extension[file_ext[1]]
                        else:
                            conversation = 'text/plain'
                        conversation = '\r\nContent-Type: '+ conversation
                        show_response += conversation
                    except:
                        status(connectionsocket, 415)
            elif state == 'Accept-Language':
                conversation = '\r\nContent-Language: ' + switcher[state]
                show_response += conversation
            elif state == 'Accept-Encoding':
                if isfile:
                    conversation = '\r\nContent-Length: ' + str(size)
                    show_response += conversation
            elif state == 'Connection':
                if isfile:
                    conn = True
                    show_response += '\r\nConnection: keep-alive'
                elif isdir:
                    conn = False
                    show_response += '\r\nConnection: close'
            elif state == 'If-Modified-Since':
                if_modify(switcher[state], entity)
            else:
                continue
        if isdir and method == 'GET':
            show_response += '\r\n\r\n'
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
            show_response = ''
            entity = CSVFILE
            fields = []
            row = []
            for d in query:
                fields.append(d)
                for i in query[d]:
                    row.append(i)
            file_exists = os.path.exists(entity)
            if file_exists:
                fi = open(entity, "a")
                show_response += 'HTTP/1.1 200 OK'
                scode = 200
                csvwriter = csv.writer(fi)
                csvwriter.writerow(row)
            else:
                fi = open(entity, "w")
                show_response += 'HTTP/1.1 201 Created'
                scode = 201
                show_response.append('Location: ' + entity)
                csvwriter = csv.writer(fi)
                csvwriter.writerow(fields)
                csvwriter.writerow(row)
            fi.close()
            show_response += '\r\nServer: ' + ip
            show_response += '\r\n'+ date()
            f = open(WORKFILE, "rb")
            show_response += '\r\nContent-Language: en-US,en'
            size = os.path.getsize(WORKFILE)
            conversation = '\r\nContent-Length: ' + str(size)
            show_response += '\r\nContent-Type: text/html'
            show_response += conversation
            show_response += '\r\n' +last_modified(entity)
            show_response += '\r\n\r\n'
            encoded = show_response.encode()
            connectionsocket.send(encoded)
            connectionsocket.sendfile(f)
        elif isfile:
            show_response += '\r\n\r\n'
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
        return [serversocket, file_extension, conditional_get, conn, ip, serverport, scode, IDENTITY]

    def response_put(self,connectionsocket, addr, ent_body, filedata, entity, switcher, f_flag, scode):
        show_response = ''
        isfile = os.path.isfile(entity)
        isdir = os.path.isdir(entity)
        try:
            length = int(switcher['Content-Length'])
        except KeyError:
            status(connectionsocket, 411)
        r = length % SIZE
        q = int(length // SIZE)
        try:
            filedata = filedata + ent_body
        except TypeError:
            ent_body = ent_body.encode()
            filedata = filedata + ent_body
        i = len(ent_body)
        size = length - i
        for _ in iter(int, 1):
            if not size > 0:
                break
            ent_body = connectionsocket.recv(SIZE)
            try:
                filedata = filedata + ent_body
            except TypeError:
                ent_body = ent_body.encode()
                filedata = filedata + ent_body
            size = size - len(ent_body)
        mode_f, r_201, move_p = True, False, False
        isdir = os.path.isdir(entity)
        isfile = os.path.isfile(entity)
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
                r = random.randint(0,4)
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
            show_response += 'HTTP/1.1 301 Moved Permanently'
            show_response += '\r\nLocation: ' + loc
        elif mode_f:
            scode = 204
            show_response += 'HTTP/1.1 204 No Content'
            show_response += '\r\n\Content-Location: ' + entity
        elif r_201:
            scode = 201
            show_response += 'HTTP/1.1 201 Created'
            show_response += '\r\nContent-Location: ' + entity
        elif not mode_f:
            scode = 501
            show_response += 'HTTP/1.1 501 Not Implemented'
        show_response += '\r\nConnection: keep-alive'
        show_response += '\r\n\r\n'
        encoded = show_response.encode()
        connectionsocket.send(encoded)

    def response_delete(self,entity, connectionsocket, ent_body, switcher, glob):
        ip, serverport,scode = glob
        show_response = ''
        isdir = os.path.isdir(entity)
        isfile = os.path.isfile(entity)
        option_list = entity.split('/')
        if 'Authorization' in switcher.keys():
            conversation = switcher['Authorization']
            conversation = conversation.split(' ')
            conversation = base64.decodebytes(conversation[1].encode()).decode()
            conversation = conversation.split(':')
            if conversation[0] == USERNAME:
                if conversation[1] == PASSWORD:
                    pass
                else:
                    scode = 401
                    show_response += 'HTTP/1.1 401 Unauthorized'
                    show_response += '\r\nWWW-Authenticate: Basic'
                    show_response += '\r\n\r\n'
                    encoded = show_response.encode()
                    connectionsocket.send(encoded)
                    return [ip, serverport, scode]
            else:
                scode = 401
                show_response += 'HTTP/1.1 401 Unauthorized'
                show_response += '\r\nWWW-Authenticate: Basic'
                show_response += '\r\n\r\n'
                encoded = show_response.encode()
                connectionsocket.send(encoded)
                return [ip, serverport, scode]
        else:
            scode = 401
            show_response += 'HTTP/1.1 401 Unauthorized'
            show_response += '\r\nWWW-Authenticate: Basic'
            show_response += '\r\n\r\n'
            encoded = show_response.encode()
            connectionsocket.send(encoded)
            return [ip, serverport, scode]
        if len(ent_body) > 1 or 'delete' in option_list or isdir:
            scode = 405
            show_response += 'HTTP/1.1 405 Method Not Allowed'
            show_response += '\r\nAllow: GET, HEAD, POST, PUT'
        elif isfile:
            scode = 200
            show_response += 'HTTP/1.1 200 OK'
            try:
                if (os.access(entity, os.W_OK)):
                    if (os.access(entity, os.R_OK)):
                        pass
                    else:
                        status(connectionsocket, 403)
                else:
                    status(connectionsocket, 403)
                shutil.move(entity, DELETE)
            except shutil.Error:
                os.remove(entity)
        else:
            scode = 400
            show_response += 'HTTP/1.1 400 Bad Request'
        show_response += '\r\nServer: ' + ip
        show_response += '\r\nConnection: keep-alive'
        show_response += '\r\n' + date()
        show_response += '\r\n\r\n'
        encoded = show_response.encode()
        connectionsocket.send(encoded)
        return [ip, serverport, scode]

m = methods()

#function to check if the resource has been modified or not since the date in HTTP request 
def if_modify(state, entity):
    global conditional_get, month
    valid = False
    if len(day) == 5:
        valid = True
    day = state.split(' ')
    if valid:
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
    return conditional_get

#function to return current date
def date():
    l = time.ctime().split(' ')
    l[0] = l[0] + ','
    conversation = (' ').join(l)
    conversation = 'Date: ' + conversation
    return conversation

#function to give response if server is busy
def status(connectionsocket, code):
    global ip, client_thread, scode
    scode = code
    show_response = ''
    if (code == '505') or (code == 505):
        show_response += 'HTTP/1.1 505 HTTP version not supported'
    elif (code == '415') or (code == 415):
        show_response += 'HTTP/1.1 415 Unsupported Media Type'
    elif (code == '403') or (code == 403):
        show_response += 'HTTP/1.1 403 Forbidden'
    elif (code == '404') or (code == 404):
        show_response += 'HTTP/1.1 404 Not Found'
    elif (code == '414') or (code == 414):
        show_response += 'HTTP/1.1 414 Request-URI Too Long'
    elif (code == '500') or (code == 500):
        show_response += 'HTTP/1.1 500 Internal Server Error'
    elif (code == '503') or (code == 503):
        show_response += 'HTTP/1.1 503 Server Unavailable'
    show_response += '\r\nServer: ' + ip
    show_response += '\r\n' + date()
    show_response += '\r\n\r\n'
    if code == 505:
        show_response += '\r\nSupported Version - HTTP/1.1 \n Rest Unsupported'
    encoded = show_response.encode()
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
    show_response = ''
    show_response += 'HTTP/1.1 304 Not Modified'
    show_response += '\r\n' + date()
    show_response += '\r\n' + last_modified(entity)
    show_response += '\r\nServer: ' + ip
    show_response += '\r\n\r\n'
    encoded = show_response.encode()
    connectionsocket.send(encoded)


#function which operates between response and requests
def bridgeFunction(connectionsocket, addr, start):
    global serversocket, file_extension, conditional_get, conn, SIZE, client_thread, scode, ip, IDENTITY, serverport
    conditional_get = False
    f_flag = 0
    filedata = b""
    conn = True
    urlflag = 0
    for _ in iter(int, 1):
        if not conn:
            break
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
            # print(req_list)
            f_flag = 1
        if len(req_list) > 1:
            # every line ends with a \r\n so for only headers it'll create ['req', '']
            pass
        else:
            # print("Error in headers\n")
            break
        try:
            log.write(((addr[0]) + '\n' + req_list[0] + '\n\n'))
        except:
            pass
        show_response = ''
        header_list = req_list[0].split('\r\n')
        header_len = len(header_list)
        ent_body = req_list[1]
        request_line = header_list[0].split(' ')
        method = request_line[0]
        entity = request_line[1]
        if (entity == favicon) or (entity == 'favicon') or (entity == 'favicon.ico'):
            entity = FAVICON
        elif entity == '/':
            entity = os.getcwd()
        entity, query = breakdown(entity)
        if (len(entity) > MAX_URL and urlflag == 0):
            status(connectionsocket, 414)
            connectionsocket.close()
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
            glob = m.response_get_head(connectionsocket, entity, switcher, query, method, 
            [serversocket, file_extension, conditional_get, conn, ip, serverport, scode, IDENTITY])

            serversocket, file_extension, conditional_get, conn, ip, serverport, scode, IDENTITY = glob
        elif method == 'POST':
            glob = m.response_post(ent_body, connectionsocket, switcher, [ip,serverport, scode])
            ip,serverport, scode = glob
        elif method == 'DELETE':
            glob = m.response_delete(entity, connectionsocket, ent_body, switcher, [ip,serverport, scode])
            ip, serverport, scode = glob
            conn = False
            connectionsocket.close()
        elif method == 'PUT':
            glob = m.response_put(connectionsocket, addr, ent_body, filedata, entity, switcher, f_flag, scode)
        else:
            method = 'Not Defined'
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
    for _ in iter(int, 1):
        connectionsocket, addr = serversocket.accept() # connectionsocket = request, addr = port,ip
        start = 0
        client_thread.append(connectionsocket)  # add connections
        if not (len(client_thread) < MAX_REQUEST):
            status(connectionsocket, 503)
            connectionsocket.close()
        else:
            start_new_thread(bridgeFunction, (connectionsocket, addr, start))
    serversocket.close()

'''
Function to handle the exit ( Ctrl+C and other signals )
'''
sig_rec = False
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    print("q for quit\n r for restart")
    sys.exit(0)



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