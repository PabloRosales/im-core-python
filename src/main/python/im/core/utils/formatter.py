
class Formatter(object):
    """
    Formats a a data object to various formats

    :param data: object to format
    """
    def __init__(self, data):
        self.data = data

    def to_xml(self, root='data', strict=True):
        xml = ['<%s>\n' % root if root else '']
        for (key, value) in self.data.items():
            if strict and value is None:
                continue
            xml.append('<%(key)s>%(data)s</%(key)s>\n' % {'key': key, 'data': value})
        if root:
            xml.append('</%s>' % root)
        xml = ''.join(xml)
        return xml

    def from_string(self, template):
        return template % self.data