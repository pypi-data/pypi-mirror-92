# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 14:46:06 2021

@author: AsheeshJanda
"""

from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package ever with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ajchoco", 
        version=VERSION,
        author="Asheesh Janda",
        author_email="<asheeshdeep.janda@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
		python_requires=">=3.5",
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first lib'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)