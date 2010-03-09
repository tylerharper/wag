#!/usr/bin/env python
import feedparser
import sys
import time
from args import options, config_file
from templates import get_rendered_string, TemplateNotFound
import filters

def main():
    d = feedparser.parse(options['url'])
    if options['show_keys']:
        print 'Example'
        for k in d.entries[0]:
            print '%s: %s' % (k, d.entries[0][k])
        sys.exit()
    if options['list']:
        for line in config_file.get_names():
            print line
        sys.exit()

    d.entries.reverse()
    number_of_entries = len(d.entries)
    if options['lines'] is None:
        options['lines'] = number_of_entries

    try:
        print get_rendered_string(options['template'], d.entries[number_of_entries-options['lines']:])
    except TemplateNotFound:
        print "%s does not appear to be a valid template in your template path" % options['template']
        sys.exit(1)
    except AttributeError:
        print "Either invalid url or invalid name"
        sys.exit(1)

    if options['follow']:
        try:
            last_entry = d.entries[-1]
            while True:
                time.sleep(options['sleep-interval'])
                
                new_entries = feedparser.parse(options['url']).entries
                
                pos = len(new_entries)
                for entry in new_entries:
                    if entry.updated_parsed > last_entry.updated_parsed:
                        pos -= 1
                    else:
                        break

                new_entries.reverse()
                
                try:
                    rendered_string = get_rendered_string(options['template'], new_entries[pos:])
                    if rendered_string != '':
                        print rendered_string
                except IndexError:
                    print 'No new value'
                    pass
                
                last_entry = new_entries[-1]

        except KeyboardInterrupt:
            sys.exit() 
        
        except IndexError:
            print "%s has no entries or is an invalid url" % options['url']
            sys.exit(1)
