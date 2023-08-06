#!/usr/bin/env python

# -*- coding: utf-8 -*-
# Copyright 2014-2016 The HyperSpyUI developers
#
# This file is part of HyperSpyUI.
#
# HyperSpyUI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpyUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperSpyUI.  If not, see <http://www.gnu.org/licenses/>.
"""
Created on Mon Nov 17 11:58:16 2014

@author: Vidar Tonaas Fauske
"""

from setuptools import setup, find_namespace_packages

from hyperspyui.version import __version__

setup(
    name='hyperspyUI',
    version=__version__,
    description='Hyperspy Graphical User Interface',
    author='Vidar Tonaas Fauske',
    author_email='vidartf+hyperspyui@gmail.com',
    url='http://github.com/hyperspy/hyperspyUI/',
    license='GPLv3',
    packages=find_namespace_packages(exclude=[
            'doc', 'bin', 'doc.*', 'hyperspyui.plugins.user_plugins']),
    install_requires=['hyperspy >= 1.4.1',
                      'hyperspy-gui-traitsui >= 1.1.1',
                      'matplotlib >= 1.3',
                      'pyqode.python >= 2.6.0',
                      'pyface >=6.0.0',
                      'autopep8',
                      'traits',
                      'traitsui >=5.2.0',
                      'qtconsole',
                      'ipykernel >=5.2.0',
                      'qtpy',
                      ],
    extras_require={
        ':sys_platform == "win32"': [
            'pywin32',
        ],
        'tests': [
            'pytest-qt',
            'pytest-cov',
            'pytest-timeout',
        ],
    },
    package_data={
        'hyperspyui':
        ['images/*.svg',
         'images/*.png',
         'images/*.ico',
         'images/icon/*.png',
         'images/icon/*.ico',
         'images/attributions.txt',
         'ipython_profile/*'],
    },
    entry_points={
        'gui_scripts': [
            'hyperspyui = hyperspyui.__main__:main',
         ]
    },
    keywords=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    long_description_content_type="text/x-rst",
    long_description=open('README.rst').read(),
    )
