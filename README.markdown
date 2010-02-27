
A happy tail.

Wagging a tail normally means happy, so why not make a cool rss feed reader that
works just like tail.

You can call tail on two types of things, names and urls. Names are setup in the
.wag.config file.  The config file must have the following layout:

Config File layout:

    name url template

name - the name you want to call from the command line
url - the rss/atom feed url
template - the file name for the jinja2 template you want have rendered by default. 
            ( you can override this will --template if you want)
           Also must be in your template_path (currently ~/.wag/)

If you need to figure out the keys to generate that template just run -k and
it will spit out the keys and example data assocaited with them.


