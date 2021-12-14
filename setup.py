from setuptools import setup

with open('requirements.txt', mode='r') as f:
    req = f.readlines()

setup(
    name='MusicOnto',
    version='0.0.1',
    description='Python package to extract Sentics values from text and adding them into an Ontology',
    author='Zoee Maryam & Pitteloud Jocelin',
    packages=['MusicOnto'],
    install_requires=[files for files in req],
)