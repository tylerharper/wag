import feedparser
import sys

try:
    d = feedparser.parse(sys.argv[1])
except IndexError:
    print "Must supply one feed"
    sys.exit(1)

d.entries.reverse()

for x in d.entries:
    print x.title, '-', x.link
    print '   ', x.summary, '\n'


