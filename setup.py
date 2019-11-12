#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup, find_packages


def get_version(*file_paths):
    """Retrieves the version from exo_mentions/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("exo_mentions", "__init__.py")

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-exo-mentions',
    version=version,
    description='Add mentions with Django',
    long_description=readme,
    author='JMarfil, Tomás Garzón, Javier Sújar',
    author_email='marfyl.dev@gmail.com, tomasgarzonhervas@gmail.com, javier.sujar@gmail.com',
    url='https://github.com/exolever/django-exo-mentions',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        'djangorestframework',
        'psycopg2-binary',
    ],
    license="MIT",
    zip_safe=False,
    keywords=['python', 'django', 'exo', 'mentions'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
