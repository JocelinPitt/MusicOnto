from setuptools import setup

with open('requirements.txt', encoding='utf8') as f:
    req = f.read().splitlines()

setup(
    name='MusicOnto',
    version='0.0.1',
    description='Python package to extract Sentics values from text and adding them into an Ontology',
    author='Zoee Maryam & Pitteloud Jocelpip install wheelin',
    author_email='jin.pitteloud@gmail.com',
    packages=['MusicOnto'],
    install_requires=req,
)