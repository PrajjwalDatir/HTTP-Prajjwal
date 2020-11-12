# https://realpython.com/python-requests/
# Writing a testing program
import requests
import sys
port = int(sys.argv[1])
url = 'http://127.0.0.1:' + str(port)

data = {'fname':'http',
    'lname':'sudo'
}
data2 = {'fname':'Prajjwal',
    'lname':'Datir'
}
getPath = '/home/maniac/HTTP-Prajjwal/test.txt'


s = requests.Session() 

'''Basic GET reqest'''
try:
    print("sending GET request...")
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
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

try:
    print("Checking Conditional GET...")
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
    print(f"Recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

postPath = "/home/maniac/HTTP-Prajjwal/output.csv"
try:
    print("sending POST request...")
    response = s.post( url+postPath, json=data)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

putPath = "/home/maniac/HTTP-Prajjwal/output.csv"
try:
    print("sending PUT request...")
    response = s.put(url+putPath, json=data2)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

delPath = "/home/maniac/HTTP-Prajjwal/testing/deleteme1"
try:
    print("sending DELETE request...")
    response = s.delete(url + delPath)
    if not response:
        if response.status_code == 401:
            print("Unauthorized User")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

headPath = "/home/maniac/HTTP-Prajjwal/test.txt"
try:
    print("sending HEAD request...")
    response = s.head(url + headPath)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')