from setuptools import find_packages, setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='textclustering',
    packages=find_packages(include=['textclustering']),
    version='0.1.1.0',
    description='Text Clustering using DBSCAN and word vectors',
    author='Arnab Borah',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
