from distribute_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages




setup(
    name='wag',
    version='0.2',
    description="Tail your rss and atom feeds",
    long_description="Make your tail happy, wag it!",
    url='http://github.com/knobe/wag',
    license='BSD',
    author="Tyler Harper",
    author_email="tyler@cowboycoding.org",
    packages= find_packages(exclude=['distribute_setup']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    install_requires=['Jinja2>=2', 'argparse>=1', 'feedparser>=4.1', 'html2text>=2'],
    entry_points={
        'console_scripts': ['wag = wag.wag:main'],
    },
)
