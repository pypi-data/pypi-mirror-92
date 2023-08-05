import setuptools
import os
import sys
import pathlib

with open("README.md","r") as fh:
    long_description = fh.read()



setuptools.setup(
    name = 'math_function',
    version='0.0.1',
    description = 'Small Calculator',
    Long_description = long_description,
    url='',
    author='Shrutika Bhapkar',
    author_email = 'shrutika01234@gmail.com',
    classifiers =[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'],
    keywords = 'calculator',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',


)