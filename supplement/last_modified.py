import os
import time

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
