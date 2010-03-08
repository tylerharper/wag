from templates import jinja_env
from html2text import html2text

def html_to_markdown(value):
    return html2text(value)

jinja_env.filters['html2markdown'] = html_to_markdown
