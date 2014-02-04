
import re

from im.core.config import configs
from im.core.utils.string import clean
from im.core.utils.formatter import Formatter

templates = {
    'xml': "<smsMessage>\n<message>%(message)s</message>\n<channelKey>%(channel_key)s</channelKey>\n<shortNumber>%(short_number)s</shortNumber>\n<phoneNumber>%(phone_number)s</phoneNumber>\n<telcoId>%(telco_code)s</telcoId>\n<systemId>%(app_id)s</systemId>\n%(tracker)s</smsMessage>",
}


class Sms(object):
    """An object that represents an SMS.
    """

    default_configuration = {
        'app_id': 0,
        'template': 'xml',
        'tokenize_regex': '[\b|,|\.| |!|\?|\'|\"]',
    }

    def __init__(self, country_code, telco_code, short_number, phone_number,
                 message, channel_key, app_id=None, use_country_code=True,
                 tracker=None, config=None, formatter=Formatter, clean=clean):

        self._config = self.default_configuration
        self._config.update(configs.get('sms', {})) 
        if config:
            self._config.update(config)

        self.telco_code = telco_code
        self.short_number = short_number
        self.phone_number = phone_number
        self.country_code = country_code
        self.message = message
        self.channel_key = channel_key
        self.app_id = app_id or self._config.get('app_id')

        self.tracker = tracker
        if tracker is not None:
            self._tracker = '<tracker>%s</tracker>\n' % tracker
        else:
            self._tracker = ''

        self._clean = clean
        self._use_country_code = use_country_code
        self._formatter = formatter
        self._serialized = None
        self._tokens = None
        self._message_clean = None

    def copy(self, message):
        return Sms(
            country_code=self.country_code,
            telco_code=self.telco_code,
            short_number=self.short_number,
            phone_number=self.phone_number,
            message=message,
            channel_key=self.channel_key,
            app_id=self.app_id,
            use_country_code=self._use_country_code,
            tracker=self.tracker,
            config=self._config,
            formatter=self._formatter,
            clean=self._clean
        )
    @property
    def full_phone_number(self):
        phone_number = self.phone_number
        if self._use_country_code:
            phone_number = '%s%s' % (self.country_code, self.phone_number)
        return phone_number

    @property
    def message_clean(self):
        if not self._message_clean:
            self._message_clean = self._clean(self.message)
        return self._message_clean

    @property
    def tokens(self):
        if not self._tokens:
            self._tokens = re.split(self._config.get('tokenize_regex'), self.message)
        return self._tokens

    @property
    def serialized(self):
        if not self._serialized:

            phone_number = self.phone_number
            if self._use_country_code:
                phone_number = '%s%s' % (self.country_code, self.phone_number)

            self._serialized = self._formatter({
                'telco_code': self.telco_code,
                'short_number': self.short_number,
                'phone_number': phone_number,
                'message': self.message_clean,
                'channel_key': self.channel_key,
                'app_id': self.app_id,
                'tracker': self._tracker,
            }).from_string(templates[self._config.get('template')])

        return self._serialized

    def __repr__(self):
        return u'Sms(%s)' % (repr({
            'country_code': self.country_code,
            'telco_code': self.telco_code,
            'short_number': self.short_number,
            'phone_number': self.phone_number,
            'message': self.message,
            'channel_key': self.channel_key,
            'app_id': self.app_id,
            'use_country_code': self._use_country_code,
            'tracker': self.tracker,
        }))

    @staticmethod
    def from_text(text, template='xml'):
        raise NotImplementedError()
