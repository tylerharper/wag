from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'wag',
    version = '0.1',
    packages= find_packages(),
    install_requires = [
        'Jinja2>=2',
        'argparse>=1',
        'feedparser>=4.1'
    ],
    entry_points = {
        'console_scripts': [
            'wag = wag.wag:main'
        ],
    },
    include_package_date = True,
    zip_safe=False
)
