# coding:utf-8
#! python3

from setuptools import setup, find_packages
from os import path

# read the contents of the README file
cur_dir = path.abspath(path.dirname(__file__))
with open(path.join(cur_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pterminal',
    version = '1.0.1',
    author = 'NimLea',
    url = 'https://github.com/nimlea/pterminal',
    packages = find_packages(),
	data_files = [("", ["LICENSE"])],
    classifiers=[
		'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
		'Programming Language :: Python :: 3',
    ],
	# project description
    long_description=long_description,
    long_description_content_type='text/markdown'
)
