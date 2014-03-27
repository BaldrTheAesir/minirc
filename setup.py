from setuptools import setup, find_packages

import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

def find_version(*file_paths):
    with codecs.open(os.path.join(here, *file_paths), 'r', 'utf-8') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\']([^'\']*)['\']",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


# Get the long description from the relevant file
with codecs.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='asyncirc',
    version=find_version('asyncirc', '__init__.py'),
    description='An asyncio based IRC library for Python 3',
    long_description=long_description,

    url='https://github.com/thibautd/asyncirc',

    author='Thibaut DIRLIK',
    author_email='thibaut.dirlik@gmail.com',

    license='GPLv3',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='irc asyncio',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires = ['colorama'],

)