from setuptools import setup, find_packages

setup(
    name='wag',
    version='0.1',
    description="Tail your rss and atom feeds",
    long_description="Make your tail happy, wag it!",
    author="Tyler Harper",
    author_email="tyler@cowboycoding.org",
    url='http://github.com/knobe/wag',
    license='BSD',
    packages= find_packages(),
    install_requires=[
        'Jinja2>=2',
        'argparse>=1',
        'feedparser>=4.1',
        'distribute',
    ],
    entry_points={
        'console_scripts': [
            'wag = wag.wag:main'
        ],
    },
    zip_safe=False,
    include_package_data=True,
    package_data={
    '':['*.py'],
    'wag':['templates/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
   ]
)
