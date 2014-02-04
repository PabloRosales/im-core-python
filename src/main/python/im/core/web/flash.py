
from collections import defaultdict

def get_flash_messages(request, clear=False):
    if not request.session:
        return {}
    messages = request.session.get('_flashes', {})
    if clear:
        clear_flash_messages(request)
    return messages


def clear_flash_messages(request):
    request.session['_flashes'] = defaultdict(list)
    request.session.modified = True


def flash(request, category, message):
    if request.session is not None:
        if not '_flashes' in request.session:
            clear_flash_messages(request)
        else:
            request.session.modified = True
        request.session['_flashes'][category].append(message)


def flash_error(request, message):
    flash(request, 'error', message)


def flash_warning(request, message):
    flash(request, 'warning', message)


def flash_notice(request, message):
    flash(request, 'notice', message)


def flash_success(request, message):
    flash(request, 'notice', message)

