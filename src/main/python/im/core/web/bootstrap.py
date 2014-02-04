
from im.core.templates.mako import Template


icons = {
    'id': 'icon-tag',
    'code': 'icon-barcode',
    'is_active': 'icon-check',
    'name': 'icon-asterisk',
    'message': 'icon-comment',
    'phone_number': 'icon-headphones',
    'gateway': 'icon-cog',
}


def combo(name, data, column, item=None, **kwargs):
    _vars = {
        'name': name,
        'data': data,
        'item': item,
        'column': column,
    }
    _vars.update(kwargs)
    return Template('core/bootstrap/combo', _vars).render()


def get_icon(name):
    if not name in icons:
        return ''
    return icons[name]