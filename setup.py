from setuptools import setup, find_packages

setup(
    name='wag',
    version="0.4",
    description="Tail your rss and atom feeds",
    long_description="Make your tail happy, wag it!",
    author="Tyler Harper",
    author_email="tyler.a.harper@gmail.com",
    url='http://github.com/knobe/wag/tree/master',
    packages=find_packages(),
    include_package_data = True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    install_requires=['Jinja2>=2', 'argparse>=1', 'feedparser>=4.1', 'html2text>=2'],
    entry_points={
        'console_scripts': ['wag = wag.shell:main'],
    },
)

