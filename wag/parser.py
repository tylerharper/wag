import feedparser
import urllib2

class InvalidJson(Exception):
    pass

try:
    import json
except ImportError:
    import simplejson as json

def jsonparse(url, default_path=''): #may need some authentication handlers
    raw_json = urllib2.urlopen(url).read()
    try:
        python_json = json.loads(raw_json)
    except ValueError:
        raise InvalidJson        
    
    if default
    
    for x in default_path:
        python_path = python_path[x]
    
    return python_path

class WagParser(object):
    def __init__(self
