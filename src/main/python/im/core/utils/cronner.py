#!/usr/bin/env python

from daemon import Daemon
from im.core.config import conf

logger = logging.getLogger('im.core.utils.cronner')

class Cronner(Daemon):
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    Original: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
    """