import argparse
import os
import config

default_config = os.environ['HOME'] + '/.wag/feeds'
default_template = 'default_rss_template'

parser = argparse.ArgumentParser(prog='wag', description='tail your rss feeds')

parser.add_argument('-n', '--lines', type=int, default=None,
                    help="The number of entries")
parser.add_argument('-t', '--template', default=None,
                    help='the template to render. REMINDER: must be in template_path')
parser.add_argument('-c', '--config', default=default_config,
                    help="Use a new config file. (default: %s)" % default_config)
parser.add_argument('-f', '--follow', action='store_true')
parser.add_argument('-s', '--sleep-interval', type=int, default=300, 
                    help='with -f, sleep for approximately N seconds (default 1.0) between iterations')
parser.add_argument('-k', '--keys', action='store_true',
                    help="prints out the valid keys for that url/name")

parser.add_argument('-l', '--list', action='store_true', help="lists all the valid names in your config file")
parser.add_argument('name', metavar='name/url', default=None)

args = parser.parse_args()
config_file = config.WagConfig(args.config)

try:
    config = config_file[args.name]
except config.NameNotInConfig:
    config = config.ConfigValue(url=args.name, template=None)

if args.template:
    config.template = args.template

if hasattr(config, 'template') == False:
    config.template = default_template

options = {}
options['url'] = config.url
options['template'] = config.template
options['follow'] = args.follow
options['lines'] = args.lines
options['show_keys'] = args.keys
options['list'] = args.list
options['sleep-interval'] = args.sleep_interval
