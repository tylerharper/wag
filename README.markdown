A Happy Tail
============

A wagging a tail normally means something is happy, so why not make a cool rss feed reader that
works just like tail.

You can call tail on two types of things, names and urls. Names are setup in the
.wag/feeds file.  The config file must have the following layout:

Config File layout:

    name url template

name - the name you want to call from the command line

url - the rss/atom feed url

template - the file name for the jinja2 template you want have rendered by default(you can override this will --template if you want).  
Also must be in your template_path (currently ~/.wag/templates and '.')

If you need to figure out the keys to generate that template just run `wag <url|name> -k` and
it will spit out the keys and example data assocaited with them.

Setting up your config and templates
------------------------------------

Ok, so I have realized that setting up your configs and templates may be a bit
confusing if you have never used any python templating engines.  We use the 
jinja2 templating engine in ours.  So for those who want to get really creative
with their templating you can read the jinja docs at 
http://jinja.pocoo.org/2/documentation/.

### Setting up that github rss feed ###

First create the directory ~/.wag and open the file ~/.wag/feed.  Put the 
following into ~/.wag/feed:

    github <your github personalized atom feed> github-template

WTF?? `github` is the name you can call from wag when you want to run it.
This makes it nice so you don't always have to put in the feed when you 
want to tail it.  `github-template` is the template that it will be looking for.
It will look for this template in your current directory and ~/.wag/templates/

Ok so to setup up that wonderful template you need access to a certain keys.
To get the keys run `wag github --keys` this will give print out the keys and
a sample of what is each key.  The format is `<key>: <example>`.  Your keys
should look something like this

    updated: 2010-03-01T11:49:20-08:00
    published_parsed: time.struct_time(tm_year=2010, tm_mon=3, tm_mday=1, tm_hour=19, tm_min=49, tm_sec=20,
    tm_wday=0, tm_yday=60, tm_isdst=0)
    subtitle: <div class="details">

      <div class="message">
                           
          friendly's description:
          <blockquote>           
            NoSQL with MySQL in Ruby
          </blockquote>             

      </div>
    </div>
    updated_parsed: time.struct_time(tm_year=2010, tm_mon=3, tm_mday=1, tm_hour=19, tm_min=49, tm_sec=20, tm
    _wday=0, tm_yday=60, tm_isdst=0)
    links: [{'href': u'http://github.com/jamesgolick/friendly', 'type': u'text/html', 'rel': u'alternate'}]
    title: rkh started watching jamesgolick/friendly
    author: rkh
    content: [{'base': 'https://github.com/knobe.private.atom?token=6bab0fd63748b7584b11b68706baf952', 'type
    ': 'text/html', 'value': u'<div class="details">\n  \n  <div class="message">\n    \n      friendly\'s d
    escription:\n      <blockquote>\n        NoSQL with MySQL in Ruby\n      </blockquote>\n    \n  </div>\n
    </div>', 'language': u'en-US'}]
    title_detail: {'base': 'https://github.com/knobe.private.atom?token=6bab0fd63748b7584b11b68706baf952', '
    type': 'text/plain', 'value': u'rkh started watching jamesgolick/friendly', 'language': u'en-US'}
    link: http://github.com/jamesgolick/friendly
    published: 2010-03-01T11:49:20-08:00
    author_detail: {'name': u'rkh'}
    id: tag:github.com,2008:WatchEvent/151460011


Nads, that is a lot of data to process.  For now just look at the first part
of each line( the words before the colons ). You have title, links and many
other keys.  We are just going to use title and links for this short intro.

So now that we have the keys lets use them.  Put the following lines into
~/.wag/templates/github-template:

    {{ title }} - {{ links[0].href }}

My friend Jeff, might think that `{{ title }}` make sense since the keys are
are the part of a hash, or dictionary in python.  Now Jeff would definatly 
question the `{{ links[0].href }}`.  Well links is a hash to an array with
another hash table in it.  So we grab the first item in the array and then use
a key from the hash.  So the output of the template would be:
    
    rkh started watching jamesgolick/friendly - http://github.com/jamesgolick/friendly

Tada now you have a basic template that will be called on all entries of your
github atom feed.

For other help please run `wag -h`
