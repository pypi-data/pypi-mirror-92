# read the contents of your README file
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
  name = 'Trading212',
  packages = ['Trading212'],
  version = '0.1.5-1',
  license='MIT',
  description = 'This package is an unofficial API for Trading212.',
  author = 'Ben Timor',
  author_email = 'me@bentimor.com',
  url = 'https://github.com/BenTimor/Trading212API/',
  download_url = 'https://github.com/BenTimor/Trading212API/archive/0.1.5.tar.gz',
  keywords = ['trading', 'trading212', 'stocks', 'money', 'api'],
  install_requires=[
          'selenium',
      ],
  classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  long_description=long_description,
  long_description_content_type='text/markdown'

)
