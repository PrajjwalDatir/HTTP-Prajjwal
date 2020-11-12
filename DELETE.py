#function to implement delete method
import os
from config import *         # import some variable values

def method_delete(element, connectionsocket, ent_body, switcher, glob):
    ip, serverport,scode = glob
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
