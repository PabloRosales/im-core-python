import sys
import logging

logger = logging.getLogger('im.core.utils.import')

def import_string(import_name, silent=False):

    """
    Imports an object based on a string. 

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """

    logger.debug('Importing %s', import_name)

    # force the import name to automatically convert to strings
    if isinstance(import_name, unicode):
        import_name = str(import_name)
    try:
        if ':' in import_name:
            module, obj = import_name.split(':', 1)
        elif '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)
        # __import__ is not able to handle unicode strings in the fromlist
        # if the module is a package
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        try:
            return getattr(__import__(module, None, None, [obj]), obj)
        except (ImportError, AttributeError):
            modname = module + '.' + obj
            __import__(modname)
            return sys.modules[modname]
    except ImportError, e:
        if not silent:
            raise ImportError(import_name, e)


            # support importing modules not yet set up by the parent module
            # (or package for that matter)