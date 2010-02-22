#!/usr/bin/env python
import os
from distutils.core import setup


def long_description():
    """
    Build the long description from a README file located in the same directory
    as this module.

    """
    base_path = os.path.dirname(os.path.realpath(__file__))
    readme = open(os.path.join(base_path, 'README'))
    try:
        return readme.read()
    finally:
        readme.close()


setup(
    name='django-compositepk',
    version='1.0',
    description='Provides a base model with rudimentary composite PK '
        'abilities.',
    long_description=long_description(),
    author='Chris Beaven',
    author_email='smileychris@gmail.com',
    url='http://bitbucket.org/smileychris/django-compositepk/',
    packages=['composite_pk'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
