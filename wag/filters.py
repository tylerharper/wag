from templates import jinja_env
from datetime import datetime, timedelta
from feedparser import _parse_date
import html2text
import time

def html_to_markdown(value, width=70):
    html2text.BODY_WIDTH = width
    return html2text.html2text(value)

def relatize(value):
    """
    
    Returns the relative time of each request.  Another feature stolen from
    github.

    How it works:
    
        get the date from value - use _parse_date from feed parser
        get current utc time.
        compare current utc time and output relative time
        
    """
    
    date_struct = _parse_date(value)[0:6]
    the_date = datetime(*date_struct)
    
    now = datetime.utcnow()
    if time.daylight:
        now = now + timedelta(hours=1)

    time_difference = now - the_date
    if time_difference.days < 0:
        return 'sometime in the near future' # just in case the time screws up
    
    if time_difference.days > 356:
        return 'about %d years ago' % (time_difference.days / 356)
    elif time_difference.days > 60:
        return 'about %d months ago' % (time_difference.days / 30)
    elif time_difference.days > 30:
        return 'about a month ago'
    elif time_difference.days > 1:
        return 'about %d days ago' % time_difference.days
    elif time_difference.days > 0:
        return 'about a day ago'
    elif time_difference.seconds > 7200:
        return 'about %d hours ago' % (time_difference.seconds / 3600)
    elif time_difference.seconds > 3600:
        return 'about an hour ago'
    elif time_difference.seconds > 120:
        return 'about %d minutes ago' % (time_difference.seconds / 60)
    elif time_difference.seconds > 60:
        return 'about a minute ago'
    elif time_difference.seconds < 60 or time_difference.days < 1:
        return 'just now'
    
    
#This could possibly go into a colors.py file
ansi_colors = {
                'bold': '1',
                'black': '30',
                'red': '31',
                'green': '32',
                'yellow': '33',
                'blue': '34',
                'magenta': '35',
                'cyan': '36',
                'white': '37',
              }

def color_func(ansi_color, bold=False):
    """This is used to fix the known closure problem"""
    color_str = "\033[%s;%sm" % (int(bold), ansi_color)
    return lambda value: color_str + value + "\033[1;m"

for color in ansi_colors:
    jinja_env.filters[color] = color_func(ansi_colors[color])
    
    if color != "bold": # thanks to sir rson
        jinja_env.filters["bold" + color] = color_func(ansi_colors[color], bold=True) 
                
jinja_env.filters['html2markdown'] = html_to_markdown
jinja_env.filters['relatize'] = relatize
