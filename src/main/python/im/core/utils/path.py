
from __future__ import absolute_import

import os
import sys

project_path = None

def get_project_path():
    if project_path is not None:
        return project_path
    if hasattr(sys.modules['__main__'], '__file__'):
        return os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
    else:
        raise Exception('Could not get project path!')

def set_project_path(path):
    global project_path
    _path = os.path.dirname(path)
    if _path not in sys.path:
        sys.path.append(_path)
    project_path = _path

