
from im.core.utils.dates import str_to_datetime, str_to_date

import argparse


types = {
    'date': str_to_date,
    'datetime': str_to_datetime,
    'int': int,
    'bool': bool,
    'str': str,
    'unicode': unicode,
    'open': open,
}


class Args(object):
    """
    Passes arguments to a defined :class:`ArgumentParser`

    :param config: Configuration object of the application
    :param parser: Argument parser callback
    """
    def __init__(self, config, parser=argparse.ArgumentParser):
        self.__config = config
        args_parser = parser(
            description=config.get('description'),
            epilog=config.get('epilog'),
            argument_default=config.get('argument_default'),
            prog=config.get('prog'),
            usage=config.get('usage')
        )
        parameters = config.get('order')
        args = config.get('args', {})

        for parameter in parameters:
            name = parameter
            params = args[parameter]
            if '_flags' in params:
                name = params['_flags']
                del params['_flags']

            if 'type' in params and params['type'] in types:
                params['type'] = types[params['type']]

            if isinstance(name, basestring):
                args_parser.add_argument(name, **params)
            else:
                args_parser.add_argument(*name, **params)

        self.args = args_parser.parse_args()
