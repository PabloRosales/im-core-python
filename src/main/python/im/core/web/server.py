
from __future__ import absolute_import

import os

from im.core.config import conf
from im.core.utils.path import get_project_path

def _get_all_files_in_dir(directory):
    files = []
    for dirpath, dirnames, filenames in os.walk(directory, followlinks=True):
        for name in filenames:
            files.append(os.path.join(dirpath, name))
    return files


def _get_local_config_files():
    return _get_all_files_in_dir(os.path.join(get_project_path(), 'configs'))


def _get_local_query_files():
    return _get_all_files_in_dir(os.path.join(get_project_path(), 'queries'))


def _get_global_config_files():
    return _get_all_files_in_dir(conf('global_config.configs_path'))

def run_development_server(app):
    from werkzeug.serving import run_simple
    extra_files = _get_local_config_files()
    extra_files.extend(_get_local_query_files())
    extra_files.extend(_get_global_config_files())
    extra_files.extend(conf('werkzeug.extra_files_autoreload', []))
    run_simple(
        app.config.get('host'),
        app.config.get('port'),
        app,
        use_debugger=app.config.get('debug'),
        use_evalex=app.config.get('evalex'),
        use_reloader=app.config.get('reloader'),
        static_files={
            app.config.get('static_url'): app.config.get('static_path'),
            '/favicon.ico': os.path.join(
                app.config.get('static_path'), 'favicon.ico'),
        },
        extra_files=extra_files,
        threaded=False
    )
