#To breakdown url in request message
from urllib.parse import *	 # for parsing URL/URI
def breakdown(entity):
    u = urlparse(entity)
    entity = unquote(u.path)
    if entity == '/':
        entity = os.getcwd()
    query = parse_qs(u.query)
    return (entity, query)
