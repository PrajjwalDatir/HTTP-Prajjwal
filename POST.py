#function to implement post method 	
import os
from config import *         # import some variable values

def method_post(ent_body, connectionsocket, switcher, glob):
    ip, serverport,scode = glob
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
