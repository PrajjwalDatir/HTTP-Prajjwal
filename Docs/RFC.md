2.7.1.  http URI Scheme
 A sender MUST NOT generate an "http" URI with an empty host
   identifier.  A recipient that processes such a URI reference MUST
   reject it as invalid.

Before making use of an "http" URI
   reference received from an untrusted source, a recipient SHOULD parse
   for userinfo and treat its presence as an error; it is likely being
   used to obscure the authority for the sake of phishing attacks.
