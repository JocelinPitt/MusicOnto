from setuptools import setup

setup(
    name='MusicOnto',
    version='0.0.1',
    description='Python package to extract Sentics values from text and adding them into an Ontology',
    author='Zoee Maryam & Pitteloud Jocelin',
    packages=['MusicOnto'],
    install_requires=[
        'requests',
        'importlib; python_version == "2.6"',
        'astunparse==1.6.3',
        'blis==0.7.5',
        'catalogue==2.0.6',
        'charset-normalizer==2.0.8',
        'click==8.0.3',
        'colorama==0.4.4'
        'cymem==2.0.6',
        'ghp-import==2.0.2',
        'idna==3.3',
        'importlib-metadata==4.8.2',
        'Jinja2==3.0.3',
        'langcodes==3.3.0',
        'langdetect==1.0.9',
        'Markdown==3.3.6',
        'MarkupSafe==2.0.1',
        'mergedeep==1.3.4',
        'mkdocs==1.2.3',
        'mkdocs-autorefs==0.3.0',
        'mkdocstrings==0.16.2',
        'murmurhash==1.0.6',
        'numpy==1.21.4',
        'Owlready2==0.35',
        'packaging==21.3',
        'pathy==0.6.1',
        'preshed==3.0.6',
        'pydantic==1.8.2',
        'pymdown-extensions==9.1',
        'pyparsing==3.0.6',
        'python-dateutil==2.8.2',
        'pytkdocs==0.12.0',
        'PyYAML==6.0',
        'pyyaml-env-tag==0.1',
        'requests==2.26.0',
        'six==1.16.0',
        'smart-open==5.2.1',
        'spacy==3.2.0',
        'spacy-legacy==3.0.8',
        'spacy-loggers==1.0.1',
        'srsly==2.4.2',
        'thinc==8.0.13',
        'tqdm==4.62.3',
        'typer==0.4.0',
        'typing-extensions==4.0.0',
        'urllib3==1.26.7',
        'wasabi==0.8.2',
        'watchdog==2.1.6',
        'zipp==3.6.0'
    ],
)