#!/usr/bin/env python
import feedparser
import sys
import time
import os
import ConfigParser
from templates import get_rendered_string, TemplateNotFound
import filters
import wagparser

default_config = os.environ['HOME'] + '/.wag/feeds'
default_template = 'default_rss_template'

def get_feed(func):
    def its_a_front(args):
        entries = feedparser.parse(args.url).entries
        entries.reverse()
        return func(args, entries)
        
    return its_a_front
        
@get_feed
def display_feed(args, entries):
    """Read the feeds once """
    number_of_entries = len(entries)
    if number_of_entries == 0:
        print "There are zero feeds for %s with url %s" % (args.name, args.url)
        sys.exit(1)

    try:
        print get_rendered_string(args.template, entries[number_of_entries-args.lines:])
    except TemplateNotFound:
        print "%s does not appear to be a valid template in your template path" % args.template
        sys.exit(1)
    except AttributeError:
        print "Either invalid url or invalid name"

wag_parser = wagparser.WagParser(display_feed, prog="wag", 
                        description="tail rss/atom feeds")

wag_parser.add_argument('-n', '--lines', type=int, default=None,
                    help="The number of entries")
wag_parser.add_argument('-t', '--template', default=None,
                    help='the template to render. REMINDER: must be in template_path')
wag_parser.add_argument('-c', '--config', default=default_config,
                    help="Use a new config file. (default: %s)" % default_config)
wag_parser.add_argument('-s', '--sleep-interval', type=int, default=300, 
                    help='with -f, sleep for approximately N seconds (default 1.0) between iterations')
wag_parser.add_argument('-v', '--verbose', action='store_true')
wag_parser.add_argument('name', metavar='name/url', default=None)

@wag_parser.arg_function('-k', '--keys', 
                         help="prints out the valid keys for that url/name")
                         
@get_feed
def show_keys(args, entries):

    for k in entries[0]:
        key_str = "'%s'" % str(k)
        #this was stolen from rson
        if args.verbose is True:
            key_str += " => '%s'" % entries[0][k]
    
        print key_str

    sys.exit()
    
@wag_parser.arg_function('-l', '--list', help="lists all the valid names in your config file")
def list(args):
    config_file = ConfigParser.RawConfigParser()
    config_file.read(args.config)
    for section in config_file.sections():
        print "'" + section + "'"
    sys.exit()

@wag_parser.arg_function('-f', '--follow')
@get_feed
def follow(args, entries):
    try:
        last_entry = entries[-1]
        while True:
            time.sleep(args.sleep_interval)
            
            new_entries = feedparser.parse(args.url).entries
            
            pos = len(new_entries)
            for entry in new_entries:
                if entry.updated_parsed > last_entry.updated_parsed:
                    pos -= 1
                else:
                    break

            new_entries.reverse()
            
            try:
                rendered_string = get_rendered_string(args.template, new_entries[pos:])
                if rendered_string != '':
                    print rendered_string
            except IndexError:
                pass
            
            last_entry = new_entries[-1]

    except KeyboardInterrupt:
        sys.exit() 
    
    except IndexError:
        print "%s has no entries or is an invalid url" % args.url
        sys.exit(1)


@get_feed
def fix_lines(args, entries):
    number_of_entries = len(entries)
    if args.lines is None:
        args.lines = number_of_entries
    
    return args

def get_config(args):

    config_file = ConfigParser.RawConfigParser()
    config_file.read(args.config)

    try:
        args.url = config_file.get(args.name, 'url')
    except ConfigParser.NoSectionError:
        args.url = args.name

    if args.template is None:
        try:
            args.template = config_file.get(args.name, 'template')
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            args.template = default_template
    
    return args
     
def main():
    result = wag_parser.run_parser([get_config, fix_lines])
    

