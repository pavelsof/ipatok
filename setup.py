import os.path

from setuptools import setup, find_packages



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'README.rst')) as f:
	README = f.read()

with open(os.path.join(BASE_DIR, 'ipatok/__version__.py')) as f:
	exec(f.read())



setup(
	name = 'ipatok',
	version = VERSION,

	description = 'IPA tokeniser',
	long_description = README,

	url = 'https://github.com/pavelsof/ipatok',

	author = 'Pavel Sofroniev',
	author_email = 'pavelsof@gmail.com',

	license = 'MIT',

	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Text Processing :: Linguistic'
	],
	keywords = 'IPA tokeniser tokenizer',

	packages = find_packages(),
	package_data = {'ipatok': ['data/*']},

	install_requires = [],

	test_suite = 'ipatok.tests'
)
