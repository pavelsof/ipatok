import os.path

from setuptools import setup, find_packages


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(BASE_DIR, 'README.rst')) as f:
    README = f.read()


with open(os.path.join(BASE_DIR, 'ipatok/__version__.py')) as f:
    exec(f.read())


setup(
    name='ipatok',
    version=VERSION,

    description='IPA tokeniser',
    long_description=README,
    long_description_content_type='text/x-rst',

    url='https://github.com/pavelsof/ipatok',
    author='pavelsof',
    author_email='mail@pavelsof.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='IPA tokeniser tokenizer',
    project_urls={
        'Changelog':
            'https://github.com/pavelsof/ipatok/blob/master/CHANGELOG.rst',
        'Source': 'https://github.com/pavelsof/ipatok',
        'Tracker': 'https://github.com/pavelsof/ipatok/issues',
    },

    packages=find_packages(),
    package_data={'ipatok': ['data/*']},

    install_requires=[],
    python_requires='>=3',

    test_suite='ipatok.tests'
)
