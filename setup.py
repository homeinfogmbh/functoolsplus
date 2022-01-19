#! /usr/bin/env python3

from setuptools import setup

DESCRIPTION = 'More higher-order functions and operations on callable objects.'

setup(
    name='functoolsplus',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    py_modules=['functoolsplus'],
    license='GPLv3',
    description=DESCRIPTION
)
