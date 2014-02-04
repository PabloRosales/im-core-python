import logging

logger = logging.getLogger('im.core.exceptions')

class GenericException(Exception):
     def __init__(self, message, code=None, loglevel=None):
        Exception.__init__(self, message)
        if code:
            code = " " + str(code)
        else:
            code = ""

        if loglevel == 'info':
            logger.info('Error%s: %s' % (code, message))
        elif loglevel == 'debug':
            logger.debug('Error%s: %s' % (code, message))
        elif loglevel == 'warn':
            logger.warn('Error%s: %s' % (code, message))
        elif loglevel == 'trace':
            logger.trace('Error%s: %s' % (code, message))
        elif loglevel == 'error':
            logger.error('Error%s: %s' % (code, message))