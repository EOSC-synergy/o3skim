#!/usr/bin/env python

"""The setup script."""
# Fix the values for the lines with 'TODO'

from setuptools import setup, find_packages
setup(
    name='cicd',  # TODO
    version="0.1.0",  # TODO
    packages=find_packages(),
    scripts=["main"],

    # Project dependencies and comments
    install_requires=[], #TODO

    package_data={ #TODO
        # # If any package contains *.txt or *.rst files, include them:
        # "package_name": ["*.extension1", "*.extension2"],
    },

    # Metadata to display on PyPI
    author="Borja Esteban",
    author_email='boressan@outlook.com',
    description="Python project template - <change in setup.py>",  # TODO
    keywords="",  # TODO
    url="https://github.com/BorjaEst/cicd",   # project home page, if any
    project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    },

    # could also include long_description, download_url, etc.
)
