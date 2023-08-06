from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'thbase/README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='thbase',
    version='1.1.1',
    description='HBase thrift2 client python API. Compatible with python2.7 and python3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Author details
    author='Yutong Sean',
    author_email='yutongsean@gmail.com',
    url='https://github.com/YutSean',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(),
    py_modules=["thbase"],
    install_requires=["thrift==0.13.0", "enum34", "typing"]
)
