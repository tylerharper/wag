from templates import jinja_env
import html2text

def html_to_markdown(value, width=70):
    html2text.BODY_WIDTH = width
    return html2text.html2text(value)

jinja_env.filters['html2markdown'] = html_to_markdown
