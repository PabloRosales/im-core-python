
from __future__ import absolute_import

import logging
import yaml

YAML_EXTENSION = 'yaml'

logger = logging.getLogger('im.core.utils')

def load_yaml(f, default=None):
    """
    Loads a YAML file if it exists, if not returns ``default``.

    :param f: The file path to load

    :para default: The value to return if unable to load the YAML file or is \
    empty
    """
    if f:
        try:
            with open(f, 'r') as yaml_file:
                y = yaml.load(yaml_file)
            if y is not None:
                return y
        except IOError:
            pass
    return default


def save_yaml(d, f):
    yaml.dump(d, f, default_flow_style=False, width=250, indent=4)
