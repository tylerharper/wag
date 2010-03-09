from templates import jinja_env
from datetime import datetime, timedelta
from feedparser import _parse_date
import html2text

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

    time_difference = now - the_date
    
    if time_difference.days > 356:
        return 'about %d years ago' % (time_difference.days / 356)
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
    elif time_difference.seconds < 60:
        return 'just now'
    
jinja_env.filters['html2markdown'] = html_to_markdown
jinja_env.filters['relatize'] = relatize
