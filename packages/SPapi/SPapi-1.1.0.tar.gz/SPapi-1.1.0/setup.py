from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

req = ['requests==2.25.1']

setup(
    name='SPapi',
    version='1.1.0',
    packages=['SPapi'],
    install_requires=req,
    author='Kreal',
    author_email='lazo12kirill@gmail.com',
    description='API for jakksoft.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
