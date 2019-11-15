import os

from setuptools import setup

NAME = 'starlette_json'
VERSION = '19.11.15'
DESCRIPTION = 'Custom json serializers for the Starlette web framework.'
URL = 'https://github.com/chrisliveseer/starlette-json'
EMAIL = 'chris@liveseer.com'
AUTHOR = 'Chris Liveseer'
REQUIRES_PYTHON = '>=3.6.0'

here = os.path.abspath(os.path.dirname(__file__))

try:
	with open(os.path.join(here, 'README.md'), encoding='utf-8') as inf:
		long_description = inf.read()
except FileNotFoundError:
	long_description = DESCRIPTION

setup(
	name=NAME,
	version=VERSION,
	author=AUTHOR,
	author_email=EMAIL,
	description=DESCRIPTION,
	long_description=long_description,
	long_description_content_type='text/markdown',
	license='BSD',
	keywords='starlette json ujson orjson rapidjson',
	url=URL,
	packages=['starlette_json'],
	platforms=['any'],
	classifiers=[
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: Implementation :: CPython',
	],
	python_requires=REQUIRES_PYTHON,
	install_requires=['starlette'],
	extra_require=[
		'orjson',
		'ujson',
		'python-rapidjson'
	],
	include_package_data=True,
)
