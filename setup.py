from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='calctex',
    packages=['calctex'],
    version='0.0.1',
    license='MIT',
    install_requires=['numpy'],
    author='shosatojp',
    author_email='me@shosato.jp',
    url='https://github.com/uec-world-dominators/calctex',
    description='Show latex formula of calclation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='calctex calc-tex calc tex latex',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)