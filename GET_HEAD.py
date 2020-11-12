import os
from config import *         # import some variable values
#function to implement get and head method
def method_get_head(connectionsocket, element, switcher, query, method, glob):
    serversocket, file_extension, conditional_get, conn, ip, serverport, scode, IDENTITY = glob
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
