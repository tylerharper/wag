import feedparser
import sys
import time
import os
import ConfigParser
from templates import get_rendered_string, TemplateNotFound
import filters

def multi_feed(func):
"""Return either all of the feeds object or just the entries"""
    def pseudo_object(self):
        for name in self.args.names:
            try:
                url = self.feeds_object.get(name, 'url')
                template = self.feeds_object.get(name, 'template')
            except ConfigParser.NoSectionError:
                url = name
                
            if self.args.template is None:
                self.args.template = template
             
            feed = feedparser.parse(url)
            feed.entires.reverse()
    
            return func(self, feed)
    return pseudo_object
            
class Wag(object):
    def __init__(self, args, feeds_object):
        self.args = args
        self.feeds_object = feeds_object

    def display_feed(self, feed):
        """Takes a list of entries from config"""
        number_of_entries = len(feed)
        if number_of_entries == 0:
            print "There are zero feeds for %s with url %s" % (self.args.name, self.args.url)
            sys.exit(1)

        try:
            print get_rendered_string(self.args.template, feed[number_of_entries-self.args.lines:])
        except TemplateNotFound:
            print "%s does not appear to be a valid template in your template path" % self.args.template
            sys.exit(1)
        except AttributeError:
            print "Either invalid url or invalid name"

    @multi_feed
    def default(self, feed):
        self.display(feed)
                         
    @mutli_feed
    def show_keys(self, feed):

        for k in feed[0]:
            key_str = "'%s'" % str(k)
            #this was stolen from rson
            if self.args.verbose is True:
                key_str += " => '%s'" % feed[0][k]
        
            print key_str

        sys.exit()
    
    def list(self):
        config_file = ConfigParser.RawConfigParser()
        config_file.read(self.args.config)
        for section in config_file.sections():
            print "'" + section + "'"
        sys.exit()

    @multi_feed
    def follow(self, feed):
        self.display_feed(feed)
        try:
            last_entry = feed[-1]
            while True:
                time.sleep(self.args.sleep_interval)
                
                new_entries = feedparser.parse(self.args.url).entries
                
                pos = len(new_entries)
                for entry in new_entries:
                    if entry.updated_parsed > last_entry.updated_parsed:
                        pos -= 1
                    else:
                        break

                new_entries.reverse()
                
                try:
                    rendered_string = get_rendered_string(self.args.template, new_entries[pos:])
                    if rendered_string != '':
                        print rendered_string
                except IndexError:
                    pass
                
                last_entry = new_entries[-1]

        except KeyboardInterrupt:
            sys.exit() 
        
        except IndexError:
            print "%s has no entries or is an invalid url" % self.args.url
            sys.exit(1)

