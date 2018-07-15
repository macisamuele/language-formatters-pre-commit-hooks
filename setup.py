from setuptools import find_packages
from setuptools import setup


setup(
    name='maci_pre_commit_hooks',
    description='Some out-of-the-box hooks for pre-commit.',
    url='https://github.com/macisamuele/pre-commit-hooks',
    version='0.0.1',

    author='Samuele Maci',
    author_email='macisamuele@gmail.com',

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        'ruamel.yaml',
        'six',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
