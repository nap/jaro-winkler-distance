__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'

from setuptools import setup, find_packages

setup_info = {
    'name': 'pyjarowinkler',
    'version': '0.1.0',
    'maintainer': __author__.split(' - ')[0],
    'maintainer_email': __author__.split(' - ')[1],
    'author': __author__.split(' - ')[0],
    'author_email': __author__.split(' - ')[1],
    'url': 'https://github.com/nap/jaro-winkler-distance',
    'license': 'http://www.apache.org/licenses/',
    'summary': 'Find the Jaro Winkler Distance which indicates the similarity score between two Strings',
    'platform': ['linux'],
    'packages': find_packages(),
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
}
setup(**setup_info)
