import feedparser
import sys
import time
import os
import ConfigParser
import filters
from templates import get_rendered_string, TemplateNotFound
from itertools import izip_longest, izip


def multi_feed(func):
    def pseudo_object(self):
        if len(self.args.names) > len(self.args.template):
            iterable_args = izip_longest(self.args.names, self.args.template)
        else:
            iterable_args = izip(self.args.names, self.args.template)

        for name, arg_template in iterable_args:
            try:
                url = self.feeds_object.get(name, 'url')
                template = self.feeds_object.get(name, 'template')
            except ConfigParser.NoSectionError:
                url = name
                template = 'default_rss_template'
            
            if arg_template is None:
                arg_template = template

            self.args.single_template = arg_template
            
            self.args.url = url
             
            feed = feedparser.parse(url)
            feed.entries.reverse()
            
            #fixing line numbers
            if self.args.lines is None:
                self.args.lines = len(feed.entries)
            
            func(self, feed)
    return pseudo_object
            
class Wag(object):
    def __init__(self, args, feeds_object):
        self.args = args
        self.feeds_object = feeds_object

    def display_feed(self, feed):
        """Takes a list of entries from config"""
        print '\n---------- %s ----------\n' % feed.feed['title']
        number_of_entries = len(feed.entries)
        if number_of_entries == 0:
            print "There are zero feeds at %s" % (self.args.url)
            sys.exit(1)

        try:
            print get_rendered_string(self.args.single_template, feed.entries[number_of_entries-self.args.lines:])
        except TemplateNotFound:
            print "%s does not appear to be a valid template in your template path" % self.args.single_template
            sys.exit(1)
        #except AttributeError:
        #    print "Either invalid url or invalid name"

    @multi_feed
    def default(self, feed):
        self.display_feed(feed)
                         
    @multi_feed
    def show_keys(self, feed):

        for k in feed.entries[0]:
            key_str = "'%s'" % str(k)
            #this was stolen from rson
            if self.args.verbose is True:
                key_str += " => '%s'" % feed.entries[0][k]
        
            print key_str

        sys.exit()
    
    def list(self):
        for section in self.feeds_object.sections():
            print "'" + section + "'"
        sys.exit()

    @multi_feed
    def _follow(self, feed):
        last_entry = feed.entries[-1]
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
                rendered_string = get_rendered_string(self.args.single_template, new_entries[pos:])
                if rendered_string != '':
                    print rendered_string
            except IndexError:
                pass
            
            last_entry = new_entries[-1]

    def follow(self):
        self.default()
        try:
            while True:
                self._follow()
        except KeyboardInterrupt:
            sys.exit()

        except IndexError:
            print "%s has no entries or is an invalid url" % self.args.url
            sys.exit(1)

