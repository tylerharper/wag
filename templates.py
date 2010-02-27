from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
import os

template_path = os.environ['HOME'] + '/.wag'
jinja_env = Environment(loader=FileSystemLoader(template_path))

def get_rendered_string(template_name, entries):
    template = jinja_env.get_template(template_name)
    string = ''
    for e in entries:
        string += template.render(**e)

    return string
