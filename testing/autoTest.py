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
getPath = '/home/maniac/Downloads/Files_Maniac/PROJECTS/04Working/HTTP-web-server-V2/MYHTTP-webserver-CN/master.py'
'''Basic GET reqest'''
try:
    print("sending GET request...")
    response = requests.get(url + getPath)
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
    response = requests.get(url + getPath)
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

postPath = "/home/maniac/Downloads/Files_Maniac/PROJECTS/04Working/HTTP-web-server-V2/MYHTTP-webserver-CN/output.txt"
try:
    print("sending POST request...")
    response = requests.post(url+postPath, json=data)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

putPath = "/home/maniac/Downloads/Files_Maniac/PROJECTS/04Working/HTTP-web-server-V2/MYHTTP-webserver-CN/output.csv"
try:
    print("sending PUT request...")
    response = requests.put(url+putPath, json=data2)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

delPath = "/home/maniac/Downloads/Files_Maniac/PROJECTS/04Working/HTTP-web-server-V2/MYHTTP-webserver-CN/output.csv"
try:
    print("sending DELETE request...")
    response = requests.delete(url + delPath)
    if not response:
        if response.status_code == 401:
            print("Unauthorized User")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

headPath = "/home/maniac/Downloads/Files_Maniac/PROJECTS/04Working/HTTP-web-server-V2/MYHTTP-webserver-CN/master.py"
try:
    print("sending HEAD request...")
    response = requests.head(url + headPath)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')