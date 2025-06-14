# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='exfactory',
    version='0.2.0',
    author='Sinngetsu',
    packages=find_packages(),
    url='https://github.com/Shinngetsu/exfactory.git',
    license='MIT',
    description='A factory for creating and managing Python objects with ease.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)