#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()


# Extras requirements for optional dependencies
extras = {
    'analysis': ['weblogo>=3.7'],
    'all': ['weblogo>=3.7']
}

# Version number must be in sync with the one in pbxplore/__init__.py
setup(
    name='pbxplore',
    version='1.4.0',

    description="PBxplore is a suite of tools dedicated to Protein Block analysis.",
    long_description=readme,

    url='https://github.com/pierrepo/PBxplore',

    # Author details
    author='Pierre Poulain',
    author_email='pierre.poulain@cupnet.net',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    setup_requires=['pytest-runner'],
    python_requires='>=3.6',
    install_requires=['numpy', 'MDAnalysis>=0.11', 'matplotlib'],
    tests_require=['pytest', 'pytest-raises', 'coverage'],
    # List additional groups of dependencies here
    # To install, use
    # $ pip install -e .[analysis]
    extras_require=extras,

    packages=find_packages(exclude=['test']),
    include_package_data=True,
    package_data={'pbxplore': ['demo/*']},

    entry_points={
        'console_scripts': [
            'PBassign = pbxplore.scripts.PBassign:pbassign_cli',
            'PBcount  = pbxplore.scripts.PBcount:pbcount_cli',
            'PBstat   = pbxplore.scripts.PBstat:pbstat_cli',
        ],
    },

)
