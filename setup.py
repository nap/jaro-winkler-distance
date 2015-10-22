__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'
__version__ = '1.7'

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox  # import here, cause outside the eggs aren't loaded
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


if sys.version_info[:2] < (2, 6):
    raise RuntimeError('pyjarowinkler requires Python 2.6 minimum')


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
    'tests_require': ['tox'],
    'cmdclass': {'test': Tox},
    'long_description': read('README.rst'),
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
}
setup(**setup_info)
