# https://realpython.com/python-requests/
# Writing a testing program
"""

show_response = ""

show_response += 'Server: ' + ip
show_response += date()
show_response += '\r\n\r\n'

encoded = show_response.encode()
connectionsocket.send(encoded)
logging.info('	{}	{}\n'.format(connectionsocket, scode))

"""

import requests
import sys
port = int(sys.argv[1])
url = 'http://127.0.0.1:' + str(port)

data = {'username':'http',
    'password':'sudo'
}
data2 = {'fname':'Prajjwal',
    'lname':'Datir'
}
getPath = '/home/maniac/HTTP-Prajjwal/test.txt'


s = requests.Session() 

'''Basic GET reqest'''
try:
    print("GET request:")
    response = s.get(url + getPath)
    '''In HTTP headers are case-insensitive so capital small doesn't matter!'''
    # response.headers
    # response.json()
    # response.encoding = 'utf-8'
    # response.text
    # response.content
    # response.headers['Content-Type']
    # response.headers['Date']
    # response.headers['Status']
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"text files opening succesfully\nstatus code: {response.status_code}\n\n")
except Exception as err:
    print(f'Other error occurred: {err}')

getPath = '/home/maniac/HTTP-Prajjwal/media/audio.mp3'
try:
    print("GET request:")
    response = s.get(url + getPath)
    '''In HTTP headers are case-insensitive so capital small doesn't matter!'''
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Media opening Succesfully\nstatus code: {response.status_code}\n")
except Exception as err:
    print(f'Other error occurred: {err}\n')

getPath = '/home/maniac/HTTP-Prajjwal/media/audio.mp3'
try:
    print("GET request:")
    response = s.get(url + getPath)
    '''In HTTP headers are case-insensitive so capital small doesn't matter!'''
    if not response:
        print("Something's Wrong!\nResponse Not Recieved")
    print(f"Media opening Succesfully\nstatus code: {response.status_code}\n")
except Exception as err:
    print(f'Other error occurred: {err}\n')


getPath = '/home/maniac/HTTP-Prajjwal/media/index.mp3'
try:
    print("GET request:")
    response = s.get(url + getPath)
    '''In HTTP headers are case-insensitive so capital small doesn't matter!'''
    # response.headers
    # response.json()
    # response.encoding = 'utf-8'
    # response.text
    # response.content
    # response.headers['Content-Type']
    # response.headers['Date']
    # response.headers['Status']
    if not response:
        print("404 coming Succesfully.")
    print(f"status code: {response.status_code}\n")
except Exception as err:
    print(f'Other error occurred: {err}')

postPath = "/home/maniac/HTTP-Prajjwal/output.csv"
try:
    print("\nsending POST request...")
    response = s.post( url+postPath, json=data)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

putPath = "/home/maniac/HTTP-Prajjwal/output.csv"
try:
    print("\nsending PUT request...")
    response = s.put(url+putPath, json=data2)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

delPath = "/home/maniac/HTTP-Prajjwal/testing/deleteme1"
try:
    print("\nsending DELETE request...")
    response = s.delete(url + delPath)
    if not response:
        if response.status_code == 401:
            print("Unauthorized User")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

headPath = "/home/maniac/HTTP-Prajjwal/test.txt"
try:
    print("\nsending HEAD request...")
    response = s.head(url + headPath)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')