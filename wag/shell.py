#!/usr/bin/env python
import ConfigParser
import argparse
from wag import Wag
import os

default_config = os.environ['HOME'] + '/.wag/feeds'
default_template = 'default_rss_template'
default_url = None

parser = argparse.ArgumentParser(prog="wag", 
                        description="tail rss/atom feeds")

parser.add_argument('-n', '--lines', type=int, default=None,
                    help="The number of entries")
parser.add_argument('-t', '--template', default=[], nargs='+',
                    help='the template to render. REMINDER: must be in template_path')
parser.add_argument('-c', '--config', default=default_config,
                    help="Use a new config file. (default: %s)" % default_config)
parser.add_argument('-s', '--sleep-interval', type=int, default=300, 
                    help='with -f, sleep for approximately N seconds (default 1.0) between iterations')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('names', metavar='name/url', default=None, nargs='*')

parser.add_argument('-k', '--keys', action='store_true',
                         help="prints out the valid keys for that url/name")
                         
parser.add_argument('-l', '--list', help="lists all the valid names in your config file")
parser.add_argument('-f', '--follow', action='store_true')


feeds_object = ConfigParser.RawConfigParser({'url': default_url, 'template': default_template})
args = parser.parse_args()
feeds_object.read(args.config)
wag = Wag(args, feeds_object)
     
opt_map = {
    'list' : wag.list,
    'keys' : wag.show_keys,
    'follow' : wag.follow,
    }

def main():
    for opt in opt_map.keys():
        if getattr(args, opt):
            getattr(wag, opt)()
        
    wag.default()

if __name__ == '__main__':
    main()
        
    

