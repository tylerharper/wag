from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from pkg_resources import resource_string
import os

template_path = os.environ['HOME'] + '/.wag/templates'
default_template_path = os.path.dirname(os.path.abspath(__file__)) + '/templates'

jinja_env = Environment(loader=FileSystemLoader(['.',template_path, default_template_path]), trim_blocks=True)

def render_single_entry(template_name, entry):
    template = jinja_env.get_template(template_name)
    return template.render(**entry)

def get_rendered_string(template_name, entries):
    string = ''
    for e in entries:
        string += render_single_entry(template_name, e)

    return string[:-1] # removing the newline

