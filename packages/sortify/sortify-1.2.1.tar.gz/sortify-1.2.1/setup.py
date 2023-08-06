from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sortify',
    version='1.2.1',
    description='A Python package containing implementation of various sorting algorithms.',
    packages=['sortify'],
    author='Aman Sharma',
    url = 'https://github.com/amansharma2910/Sortify',
    author_email='amansharma2910@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
)