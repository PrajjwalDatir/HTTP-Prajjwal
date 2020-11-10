from socket import *         # to implement webserver
from datetime import *		 # to implement conditional get
import os					 # to use basic facilities of checking path,file, directory
import time					 # to implement conditional get
import random				 # to implement randomness so that some of the status codes get implemented
import threading			 # to handle requests coming to server
from urllib.parse import *	 # for parsing URL/URI
from _thread import *
import shutil				 # to implement delete method
import mimetypes			 # for getting extensions as well as content types
import csv					 # used in get and post method to insert the data into file
import base64				 # used for decoding autherization header in delete method
import sys					 # for arguements, exits
import logging				 # for logging
from config import *

serversocket = socket(AF_INET, SOCK_STREAM)
s = socket(AF_INET, SOCK_DGRAM)
logging.basicConfig(filename = LOG, level = logging.INFO, format = '%(asctime)s:%(filename)s:%(message)s')
