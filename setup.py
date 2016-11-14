from setuptools import setup, find_packages
import os
import platform

DESCRIPTION = "A simple lightweight python wrapper for the Azure Bing Search API."
VERSION = '0.0.1'
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    "Programming Language :: Python :: 2",
    'Topic :: Software Development :: Libraries :: Python Modules',
]

KEYWORDS = ['Azure', 'Bing', 'API', 'Search', 'Cognitive Services', 'v5']

INSTALL_REQUIRES = [
    'requests',
    'fake_useragent',
]

setup(
    name='py-cog-serv',
    #packages = ['py_bing_search'],
    packages = find_packages(),
    version=VERSION,
    author=u'Rob Truxal',
    author_email='rtruxal2020@outlook.com',
    url='https://github.com/rtruxal/py-cog-serv',
    license='MIT',
    keywords=KEYWORDS,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    test_suite='nose.collector',
    tests_require=['nose'],
)