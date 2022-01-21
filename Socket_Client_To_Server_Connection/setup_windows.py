#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 10:18:25 2019

@author: robert.shyroian
"""

import sys
from cx_Freeze import setup, Executable

include_files = ['autorun.inf']
base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name = 'client',
      version = '0.1',
      description = 'client connection',
      options = {'build_exe' : {'include_files' : include_files}},
      executables = [Executable('client.py', base = base)])