from setuptools import setup, find_packages

from codecs import open
from os import path

from jgrepl.repl import VERSION

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='jgrepl',
        version=VERSION,
        description='Extensible command-line REPL for interacting with JSON-graphs containing business objects',
        long_description=long_description,
        url='https://github.com/a115/json-graph-repl',
        author='Jordan Dimov',
        author_email='jdimov@mlke.net',
        license='MIT',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Other/Nonlisted Topic'
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            ],
        keywords='json graph repl cmd2 business',
        packages=['jgrepl',],
        install_requires=[
            'Cmd2>=0.7.5',
            ],
        entry_points={
            'console_scripts': [
                'jgrepl=jgrepl.jgrepl:main',
                ],
            }
        )
