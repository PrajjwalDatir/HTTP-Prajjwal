# HTTP Webserver From Scratch
## Implemented RFC of HTTP using SOCKET programming in python3


### HOW TO RUN

main file cotaining the code => httpserver.py

#### To run main file with restart,start, quit functionality running in SEPARATE window
    bash master.sh
#### To run main file with restart,start, quit functionality running in SAME window
    python3 master.py port_number

#### To Test the program Run
    python3 testing/autoTest.py 5562


# HTTP-Web-Server
This is the project based on http protocol that has been used in day to day life. All dimensions are considered according to rfc 2616

It has following features:-

HTTP: GET, POST, PUT, HEAD, DELETE, Cookies, Headers, non-persistent connections, Multiple clients at the same time
(with a sepearate program to test this), logging with levels of logging, handling file permissions;  Server configuration 
config file with DocumentRoot, log file name, max simulateneous connections ; way to stop and restart the server;

It is developed using socket programming and very basic level of python.
Project Developer has only focused on the quality of the server and not the features of the python language. 

Those having beginner level of knowledge about socket Programming and Python language are requested to see and understand
the code as the developer also has the beginner level of knowledge in both

> ### Minimum  Expectations from Projects
	For all projects, the commands should follow unix conventions. 
	That is, the use of hyphenated options (e.g. ls -a)  and 
	arguments on the command line (e.g. ls /tmp/) should be supported. 
	The default behavior of each software should be like the existing tools.
	
	HTTP Server
	Reference: https://tools.ietf.org/html/rfc2616
	GET, POST, PUT, HEAD, DELETE, Cookies, Headers, non-persistent connections, 
	Multiple clients at the same time (with a sepearate program to test this), 
	logging with levels of logging, handling file permissions;  
	Server configuration - config file with DocumentRoot, log file name, max simulateneous connections; 
	way to stop and restart the server;
	
	Marks : Basic HTTP 5 method = 15 marks; MT = 3 marks; 
	Config file and handling = 3 marks; cookies = 2 marks; log = 3 marks;  
	file permissions = 1 marks; Automated Testing = 3 marks.

### Here's PseudoCode I refered to while building HTTP server. 
```python
webserver {
	open a socket, bind to port 90
	listen
	t = accept();
	create a thread for t
	thread {
		s -> socket to exchange data for this particular connection
		loop {
			d = recvdata();
			interprete the data in d; // headers are to be deciphered
				string processing, tokenizing, making sense of data
				loop {
					l = next line();
					t = ':' separated list of tokens from l;
					swithch(t) {
						"Host": do something;
							carry some action on the server side;
							change some headers in the output (sent to browser);
						"User-Agent": do something;
						"GET":
							f = get the next part of "GET" // filename;
							open f;
							write HTTP headers into the socket;
							dump file f() into the socket;
						"if-modified-since":
							ht = get the 'time' given in header;
							ct = get current time;
							ft = get the time when file was modified;
							if(ft - ct < ht)
								just send headers in socket
							else
								send headers + file in socket;	
					}
				}	
		}	
	}
}

```
