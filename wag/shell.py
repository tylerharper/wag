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
parser.add_argument('-k', '--keys', action='store_true',
                         help="prints out the valid keys for that url/name")
parser.add_argument('-l', '--list', action='store_true', help="lists all the valid names in your config file")
parser.add_argument('-f', '--follow', action='store_true')
parser.add_argument('-u', '--update-feeds', type=str, help="add the current url and template to config")
parser.add_argument('--all', action='store_true', help="displays all of your feeds in your feeds file")
parser.add_argument('-e', '--exclude', default=[] ,nargs='+', help="exclude the certain feeds when you display all")
parser.add_argument('names', metavar='name/url', default=None, nargs='*')


feeds_object = ConfigParser.RawConfigParser({'template': default_template})
args = parser.parse_args()
feeds_object.read(args.config)
wag = Wag(args, feeds_object)
     
# order matters here
opt_map = [
    ('list', wag.list),
    ('update_feeds', wag.update),
    ('keys', wag.show_keys),
    ('all', wag.all),
    ('exclude', wag.exclude),
    ('follow', wag.follow),
    ]

def main():
    for opt, func in opt_map:
        if getattr(args, opt):
            func()

    wag.default()

if __name__ == '__main__':
    main()
        
    

