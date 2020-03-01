from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='calctex',
    packages=find_packages(),
    version='1.0.7',
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
    python_requires='>=3.6'
)
