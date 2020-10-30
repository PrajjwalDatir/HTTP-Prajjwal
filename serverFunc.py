from socket import *
from threading import *
from datetime import *
import os.path, time
from urllib.parse import *
import shutil
import config
import getpass
import os

# Class defined for headers manipulation of response object ; 
# To be sent to the client
class Response:	
    status = config.status_codes
	file_format = config.FORMAT
	html_string_for_post = config.post_string

	def __init__(self, request):
		self.response = "HTTP/1.1 " + "\r\n"
		self.response += "Date: " + curr_time() + "\r\n"
		self.response += "Server: Local" + "\r\n"

	'''All the methods starting with 'handle_status' are used to handle the headers required for the 
	given status code. Only 'handle_4xx' handles the response status codes starting with 4.'''
	def handle_200(self, request): 
		filename, file_extension = os.path.splitext(request["resource"])
		file_format_header = self.file_format.get(file_extension, None)
		if not file_format_header:
			return None
		index = self.response.find("\r\n")
		self.response = self.response[:index] + "200 " + self.status[200] + self.response[index:]
		self.response += "Last-Modified: " + modified(request["resource"]) + "\r\n"
		self.response += "User-Agent: " + request['User-Agent'] + "\r\n"
		self.response += "Content-type: " + file_format_header + "\r\n"
		self.response += "Connection: " + request["Connection"] + "\r\n"
		return self.response

	def handle_201(self, request):
		index = self.response.find("\r\n")
		self.response = self.response[:index] + "201 " + self.status[201] + self.response[index:]
		self.response += "Content-type: text/html" + "\r\n"
		self.response += "Location: http://" + request['Host'] + '/' + request['resource'] + "\r\n"
		self.response += "Connection: " + request["Connection"] + "\r\n"
		self.response += "Content-Length: " + str(len(self.html_string_for_post)) + "\r\n\r\n"
		self.response += self.html_string_for_post
		return self.response

	def handle_202(self, request):
		index = self.response.find("\r\n")
		self.response = self.response[:index] + "202 " + self.status[202] + self.response[index:]
		self.response += "Connection: " + request["Connection"] + "\r\n"
		return self.response

	def handle_204(self, request):
		index = self.response.find("\r\n")
		self.response = self.response[:index] + "204 " + self.status[204] + self.response[index:]
		self.response += "Connection: " + request["Connection"] + "\r\n\r\n"
		return self.response

	def handle_304(self, request):
		index = self.response.find("\r\n")
		self.response = self.response[:index] + "304 " + self.status[304] + self.response[index:]
		self.response += "Connection: " + request["Connection"] + "\r\n"
		self.response += "Last-Modified: " + modified(request["resource"]) + "\r\n"
		return self.response

	def handle_4xx(self, request, stat):
		f = str(stat) + ".html"
		index = self.response.find("\r\n")
		self.response = self.response[:index] + str(stat) + " " + self.status[stat] + self.response[index:]
		try:
			file = open(f, "r")
			entity = file.read()
			file.close()
			l = len(entity)
		except:
			print("The status file could not be opened")
		self.response += "Content-Length: " + str(l) + "\r\n"
		self.response += "Content-type: text/html" + "\r\n\r\n"
		self.response += entity
		return self.response

	def handle_405(self, request):
		index = self.response.find("\r\n")
		self.response = self.response[:index] + str(stat) + " " + self.status[stat] + self.response[index:]
		return self.response

	def handle_501(self, request):
		index = self.response.find("\r\n")
		self.response = self.response[:index] + "501 " + self.status[501] + self.response[index:]
		file = open("501.html", "r")
		entity = file.read()
		file.close()
		l = len(entity)
		self.response += "Content-Length: " + str(l) + "\r\n"
		self.response += "Content-type: text/html" + "\r\n\r\n"
		self.response += entity
		return self.response

	def handle_505(self, request):
		index = self.response.find("\r\n")
		self.response = self.response[:index] + "505 " + self.status[505] + self.response[index:] + "\r\n"
		return self.response


#returns the current time in the required format
def curr_time():
		t = datetime.now()
		t = t.strftime("%a, %d %b %Y %H:%M:%S")
		return t

#gets the modified time of file
def modified(file_path): 
	t = os.path.getmtime(file_path)
	t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t)) + " GMT"
	return t

# CREATES SERVER TO LISTEN TO CLIENTS 
class server:
    methods = config.methods
    authPassword = config.authPassword
    def __init__(self, address):
        try:
            #create a TCP socket
            server_socket = socket.server_socket(AF_INET, SOCK_STREAM)
        except:
            print("Socket could not be created")
            return None
        #Binds the socket to the given address
        server_sock.bind(address)
		self.start_server(server_sock)
    
    # Start the server
    def start_server(self, server_sock):
		print("Voila! Server is running..\n" + "Press ctrl + c to quit")
        #Starts listening for tcp connection
        server_sock.listen(100)
		while True:
			new_connection, recv_addr = server_sock.accept() #Connect to the requesting client
			'''The following line creates a thread for each new requesting client'''
			client = Thread(group = None, target = self.run, kwargs = {'new_connection' : new_connection, 'recv_addr' : recv_addr})
			#Start the thread dedicated to requests only from the given client
            client.start()






















if __name__ == '__main__':
    #obtain address from the configuration file
	address = config.address
    # Create server object
	new_server = server(address)
    if new_server is None:
        print("Please Restart the Server")
        return