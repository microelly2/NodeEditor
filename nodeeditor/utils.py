# common utilities for use in many files

'''
from nodeeditor.utils import *

'''

import nodeeditor.config as config

# reload for development
import sys
if sys.version_info[0] !=2:
	from importlib import reload



def devmode():
    ''' more details for development'''
    return config.dev
