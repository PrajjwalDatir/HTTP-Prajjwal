import os
from config import *         # import some variable values

#function to implement put method
def method_put(connectionsocket, addr, ent_body, filedata, element, switcher, f_flag, scode):
    display = []
    isfile = os.path.isfile(element)
    isdir = os.path.isdir(element)
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
    isfile = os.path.isfile(element)
    isdir = os.path.isdir(element)
    l = len(element)
    limit = len(ROOT)
    if l >= limit:
        if isdir:
            if os.access(element, os.W_OK):
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
            if os.access(element, os.W_OK):
                pass
            else:
                status(connectionsocket, 403)
            mode_f = True
            if f_flag == 0:	
                f = open(element, "w")
                f.write(filedata.decode())
            else:
                f = open(element, "wb")
                f.write(filedata)
            f.close()
        else:
            #r = random.randint(0,4)
            if ROOT in element:
                r_201 = True
                element = ROOT + '/' + str(addr[1])
                try:
                    element = element + file_type[switcher['Content-Type'].split(';')[0]]
                except:
                    status(connectionsocket, 403)
                if f_flag == 0:	
                    f = open(element, "w")
                    f.write(filedata.decode())
                else:
                    f = open(element, "wb")
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
        display.append('HTTP/1.1 301 Moved Permanently')
        display.append('Location: ' + loc)
    elif mode_f:
        scode = 204
        display.append('HTTP/1.1 204 No Content')
        display.append('Content-Location: ' + element)
    elif r_201:
        scode = 201
        display.append('HTTP/1.1 201 Created')
        display.append('Content-Location: ' + element)
    elif not mode_f:
        scode = 501
        display.append('HTTP/1.1 501 Not Implemented')
    display.append('Connection: keep-alive')
    display.append('\r\n')
    return display
