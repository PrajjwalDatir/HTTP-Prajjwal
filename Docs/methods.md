### HTTP - Parameters https://www.tutorialspoint.com/http/http_parameters.htm  
    HTTP Version
    Uniform Resource Identifiers
    Date/Time Formats
    Character Sets
    Content Encodings
    Media Types
    Language Tags

### HTTP - Messages https://www.tutorialspoint.com/http/http_messages.htm
    Message Start-Line
    Header Fields
    Message Body

### HTTP - Requests https://www.tutorialspoint.com/http/http_requests.htm
    Request-Line
    Request Method
    Request-URI
    Request Header Fields

##### Methods and their Description
    1. GET
    The GET method is used to retrieve information from the given server using a given URI. Requests using GET should only retrieve data and should have no other effect on the data.

    2. HEAD
    Same as GET, but it transfers the status line and the header section only.

    3. POST
    A POST request is used to send data to the server, for example, customer information, file upload, etc. using HTML forms.

    4. PUT
    Replaces all the current representations of the target resource with the uploaded content.

    5. DELETE
    Removes all the current representations of the target resource given by URI.

##### Additional information
    - Accept-Charset
    - Accept-Encoding
    - Accept-Language
    - Authorization
    - Expect
    - From
    - Host
    - If-Match
    - If-Modified-Since
    - If-None-Match
    - If-Range
    - If-Unmodified-Since
    - Max-Forwards
    - Proxy-Authorization
    - Range
    - Referer
    - TE
    - User-Agent


### Example Requests

##### General Get Request
    GET /hello.htm HTTP/1.1
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    Host: www.tutorialspoint.com
    Accept-Language: en-us
    Accept-Encoding: gzip, deflate
    Connection: Keep-Alive
</br>

##### Posting general example
    POST /cgi-bin/process.cgi HTTP/1.1
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    Host: www.tutorialspoint.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: length
    Accept-Language: en-us
    Accept-Encoding: gzip, deflate
    Connection: Keep-Alive

    licenseID=string&content=string&/paramsXML=string

</br>

##### Posting xml file
    POST /cgi-bin/process.cgi HTTP/1.1
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    Host: www.tutorialspoint.com
    Content-Type: text/xml; charset=utf-8
    Content-Length: length
    Accept-Language: en-us
    Accept-Encoding: gzip, deflate
    Connection: Keep-Alive

    <?xml version="1.0" encoding="utf-8"?>
    <string xmlns="http://clearforest.com/">string</string>

### HTTP - Responses
    HTTP Version
    Status Code
    Response Header Fields
    Accept-Ranges
    Age
    ETag
    Location
    Proxy-Authenticate
    Retry-After
    Server
    Vary
    WWW-Authenticate

##### Examples of Response Message
    
    HTTP/1.1 200 OK
    Date: Mon, 27 Jul 2009 12:28:53 GMT
    Server: Apache/2.2.14 (Win32)
    Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
    Content-Length: 88
    Content-Type: text/html
    Connection: Closed

    <html>
    <body>
    <h1>Hello, World!</h1>
    </body>
    </html>
