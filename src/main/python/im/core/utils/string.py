
import unicodedata


def clean(message):
    return unicodedata.normalize('NFKD', unicode(message)).encode('ascii', 'ignore')

