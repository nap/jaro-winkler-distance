__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'
__version__ = '0.1.1'

import os
import sys
from setuptools import setup, find_packages


if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    sys.exit('Sorry, Python < 2.7 is not supported')


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
    'long_description': read('README.rst'),
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
