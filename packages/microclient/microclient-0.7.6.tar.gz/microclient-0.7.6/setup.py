from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='microclient',
    version='0.7.6',
    description='A library for creating REST API clients quick and painless.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/biinsight/microclient/',
    author='Szymon Nowak',
    author_email='snowak@biinsight.pl',
    license='',
    packages=['microclient'],
    install_requires=['requests',
                      'loguru',
                      ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
