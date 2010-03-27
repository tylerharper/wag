import feedparser
import sys
import time
import os
import ConfigParser
import filters
import urlparse
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
            
            
            parsed_url = urlparse.urlparse(url)
            # add http:// if url is reddit.com instead of http://reddit.com
            # url parse messes up sometimes so I need to specfiy
            # also urllib2 in feedparser only supports http, https, ftp, ftps
            if parsed_url.scheme.lower() not in ['http', 'https', 'ftp', 'ftps']:
                url = 'http://' + url

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
        self.last_update_time = {}
        self.last_updated_feed = ''

    def _fix_url(self):
        """Fixes mangled urls"""

    def display_feed(self, feed):
        """Takes a list of entries from config"""
        if len(self.args.names) > 1: # print title if more than one feed specified
            print '\n---------- %s ----------' % feed.feed.get('title', self.args.url)

        number_of_entries = len(feed.entries)
        if number_of_entries == 0:
            print "There are zero feeds at %s" % (self.args.url)
            sys.exit(1)

        try:
            print get_rendered_string(self.args.single_template, feed.entries[number_of_entries-self.args.lines:])
        except TemplateNotFound:
            print "%s does not appear to be a valid template in your template path" % self.args.single_template
            sys.exit(1)
        except IOError:
            pass
        #except AttributeError:
        #    print "Either invalid url or invalid name"

    @multi_feed
    def default(self, feed):
        self.display_feed(feed)
                         
    @multi_feed
    def show_keys(self, feed):

        for k in feed.entries[-1]:
            key_str = "'%s'" % str(k)
            #this was stolen from rson
            if self.args.verbose is True:
                key_str += " => '%s'" % feed.entries[-1][k]
        
            print key_str

        sys.exit()
    
    def list(self):
        for section in self.feeds_object.sections():
            print "'" + section + "'"
        sys.exit()

    
    def all(self):
        self.args.names = self.feeds_object.sections()

    def exclude(self):
        new_names = set(self.args.names).difference(self.args.exclude)
        self.args.names = list(new_names)
    
    def update(self):
        if len(self.args.names) > 1:
            print 'wag: only one url per update'
            sys.exit(1)

        elif len(self.args.template) > 1:
            print 'wag: only one template per update'
            sys.exit(1)
        
        name = self.args.update_feeds

        try:
            self.feeds_object.add_section(name)
        except ConfigParser.DuplicateSectionError:
            pass
    
        if len(self.args.names) > 0:
            self.feeds_object.set(name, 'url', self.args.names[0])
        
        if len(self.args.template) > 0:
            self.feeds_object.set(name, 'template', self.args.template[0])
        
        #added everything just making sure its parsable
        if self.feeds_object.has_option(name, 'url') == False:
            print 'wag: configs must have a url'
            sys.exit(1)

        with open(self.args.config, 'wb') as configfile:
            self.feeds_object.write(configfile)
    
        print 'wag: updated %s successfully' % self.args.update_feeds
        sys.exit()
            

    @multi_feed
    def _follow_first_display(self, feed):
        """
        This function allows us to store the last entries update time.
        Oh and it also displays the feed.
        """
        self.display_feed(feed)
        self.last_update_time[self.args.url] = feed.entries[-1].updated_parsed
        self.last_updated_feed = self.args.url
        
    @multi_feed
    def _follow(self, feed):
        new_entries = feedparser.parse(self.args.url).entries
        
        pos = len(new_entries)
        for entry in new_entries:
            if entry.updated_parsed > self.last_update_time[self.args.url]:
                pos -= 1
            else:
                break

        new_entries.reverse()
        
        try:
            rendered_string = get_rendered_string(self.args.single_template, new_entries[pos:])
            if rendered_string != '':
                if self.last_updated_feed != self.args.url:
                    print '\n---------- %s ----------' % feed.feed.get('title', self.args.url)
                    self.last_updated_feed = self.args.url

                print rendered_string
        except IndexError:
            pass
        
        self.last_update_time[self.args.url] = new_entries[-1].updated_parsed

    def follow(self):
        self._follow_first_display()
        try:
            while True:
                time.sleep(self.args.sleep_interval)
                self._follow()
        except KeyboardInterrupt:
            sys.exit()

        except IndexError:
            print "%s has no entries or is an invalid url" % self.args.url
            sys.exit(1)

