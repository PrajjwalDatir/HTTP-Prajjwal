# https://realpython.com/python-requests/
# Writing a testing program
import requests
import sys
port = int(sys.argv[1])
url = 'http://127.0.0.1:' + str(port)

getPath = None
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

postPath = None
try:
    print("sending POST request...")
    response = requests.post(url+postPath, data={'key':'value'})
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

putPath = None
try:
    print("sending PUT request...")
    response = requests.put(url+putPath, data={'key':'value'})
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

delPath = None
try:
    print("sending DELETE request...")
    response = requests.delete(url + delPath)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')

headPath = None
try:
    print("sending HEAD request...")
    response = requests.head(url + headPath)
    if not response:
        print("Something's Wrong!\nResponse Not Recieved.")
    print(f"Response recieved with status code: {response.status_code}")
except Exception as err:
    print(f'Other error occurred: {err}')