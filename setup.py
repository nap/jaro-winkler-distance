__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'
__version__ = '0.1.0'

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup_info = {
    'name': 'pyjarowinkler',
    'version': __version__,
    'maintainer': __author__.split(' - ')[0],
    'maintainer_email': __author__.split(' - ')[1],
    'author': __author__.split(' - ')[0],
    'author_email': __author__.split(' - ')[1],
    'url': 'https://github.com/nap/jaro-winkler-distance',
    'download_url': "https://github.com/nap/jaro-winkler-distance/archive/v{0}.zip".format(__version__),
    'license': 'http://www.apache.org/licenses/',
    'description': 'Find the Jaro Winkler Distance which indicates the similarity score between two Strings',
    'platforms': ['Linux'],
    'keywords': 'jaro winkler distance score string delta diff',
    'packages': find_packages(),
    'long_description': read('README.md'),
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
