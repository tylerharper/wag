from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name='wag',
    version='0.1',
    description="Tail your rss and atom feeds",
    packages= find_packages(),
    install_requires=[
        'Jinja2>=2',
        'argparse>=1',
        'feedparser>=4.1'
    ],
    entry_points={
        'console_scripts': [
            'wag = wag.wag:main'
        ],
    },
    include_package_data=True,
    package_data={
    'wag':['templates/*'],
    }
)
