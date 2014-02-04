import logging
import urlparse

from werkzeug.utils import redirect
from werkzeug.exceptions import abort
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.wrappers import BaseResponse, Response

from im.core.config import conf
from im.core.web.flash import flash
from im.core.database.mysql import sessions
from im.core.templates.mako import Template
from im.core.web.controller import Controller
from im.core.utils.pagination import Pagination

logger = logging.getLogger('im.core.web.crud')


class InstanceController(Controller):
    instance = None

    def __init__(self, request=None):
        super(InstanceController, self).__init__(request)
        self._url = conf('werkzeug.mount_point', '/')
        if self.instance is None:
            self.instance = conf('crud.force_instance', None)

    def _instance_selection(self, request):
        flash(request, 'error', 'Seleccione una instancia.')
        return Template('crud_instance_selection', {
            'instances': conf('crud.instances.%s' % conf('config.app')),
            'body_class': 'instance_selection',
            'title': conf('config.name'),
            'subtitle': 'Seleccion de instancia'
        })

    def _change_instance(self, request):
        change_instance = request.args.get('change_instance')
        if change_instance and int(change_instance) == 1:
            request.session['instance'] = None
            abort(Response(
                self._instance_selection(request),
                mimetype='text/html')
            )

    def _initialize(self, request, *args):
        self._change_instance(request)

        app_instance = '%s.instance' % conf('config.app')
        if self.instance:
            request.session[app_instance] = self.instance
            instance_name = self.instance
        else:
            instance_name = request.args.get('instance', None)
            if not instance_name:
                instance_name = request.session.get(app_instance, None)
            if instance_name:
                request.session[app_instance] = instance_name
            else:
                abort(Response(
                    self._instance_selection(request),
                    mimetype='text/html')
                )

        self.instance_name = instance_name
        self.instance_config = conf('crud.instances.%s.%s' % (
            conf('config.app'),
            self.instance_name
            ))

        self._get_database()
        self._get_session()

    def _get_database(self):
        self.database = self.instance_config.get('database', self.instance_name)

    def _get_session(self):
        self.session = sessions.get(self.database)


class CrudBase(InstanceController):
    toolbar = None
    template_decorator = None

    def __init__(self, model, query=None, template_decorator=None):
        self.model = model
        self._query = query
        self.template_decorator = template_decorator
        super(CrudBase, self).__init__()

    def _initialize(self, request, *args):
        super(CrudBase, self)._initialize(request, *args)

        if self._query:
            self.query = self._query(request, self.session, *args)
        else:
            if self.model is not None:
                self.query = self.session.query(self.model)

    def _get_model_columns(self, query=None):
        if query:
            if isinstance(query, list):
                try:
                    return list(query[0].__table__.columns)
                except AttributeError:
                    return list(self.model.__table__.columns)
            else:
                return list(query.__table__.columns)
        else:
            return list(self.model.__table__.columns)

    def _get_model_pk(self):
        return [i.name for i in self.model.__table__.columns if i.primary_key][0]

    def __validate__(self, request, columns, session, item):
        return True

    def _save_from_post(self, request, columns, session, item=None):

        is_update = item is not None
        obj = item if is_update else self.model()

        original_values = {}
        primary_key = None
        for column in columns:
            if column.primary_key:
                primary_key = column.name
            if column.name in request.form:
                if is_update:
                    original_values[column.name] = getattr(obj, column.name)
                if column.nullable and not request.form[column.name]:
                    setattr(obj, column.name, None)
                else:
                    setattr(obj, column.name, request.form[column.name])

        if is_update and hasattr(obj, '__pre_update__'):
            obj.__pre_update__(request, session, original_values)
        elif not is_update and hasattr(obj, '__pre_insert__'):
            obj.__pre_insert__(request, session)

        try:
            message = self.__validate__(request, columns, session, item)
            if message and not isinstance(message, basestring):
                session.begin()
                session.add(obj)
                session.commit()
            elif isinstance(message, basestring):
                flash(request, 'error', 'Hubo un error al guardar. %s' % message)
                return
        except OperationalError, e:
            session.rollback()
            flash(request, 'error', 'Hubo un error al guardar. %s' % e)
            logger.error(e)
        else:
            if item is None:
                flash(request, 'success', 'Creado exitosamente')
                id = getattr(obj, primary_key)
                return redirect('%s/../../update/%s' % (request.base_url, id))
            else:
                flash(request, 'success', 'Guardado exitosamente')
        return obj


class ReportList(CrudBase):
    instance = None

    def __init__(self, model, name, columns, headers=None, query=None,
                 subtitle=None, search_type=None, download_csv=False):
        super(ReportList, self).__init__(model, query=query)
        self.subtitle = subtitle
        self.search_type = search_type
        self.name = name
        self.headers = headers
        self.columns = columns
        self.download_csv = download_csv

    def _get_data(self, request):
        return None

    def _render(self, request, items):
        template_format = request.args.get('format', 'html')
        abort(Response(Template('crud_report_list', {
            'body_class': 'crud_report_list %s' % self.instance_name,
            'title': self.instance_config['name'],
            'subtitle': self.name + self.subtitle,
            'items': items,
            'headers': self.headers,
            'columns': self.columns,
            'base_url': self._url,
            'model': self.model,
            'search_term': request.args.get('search', None),
            'search_term_end': request.args.get('search2', None),
            'search_type': self.search_type,
            'download_csv': self.download_csv,
            }, _format=template_format), mimetype='text/%s' % template_format))

    def __call__(self, request, *args):
        self._initialize(request, *args)
        items = self._get_data(request)
        if items is None and self.model:
            items = self.query.all()

        if callable(self.subtitle):
            self.subtitle = '. ' + self.subtitle(request, *args)

        return self._render(request, items)


class CrudList(CrudBase):
    title = None
    subtitle = None
    extra_filters = None

    def __init__(self, model, query=None, read_only=False):
        super(CrudList, self).__init__(model, query=query)
        self.read_only = read_only

    def __call__(self, request, *args):
        search_term = request.form.get('search', None)

        self._initialize(request, *args)

        if  search_term is not None and hasattr(self.model, 'search'):
            search_term = urlparse.unquote(search_term)
            self.query = self.model.search(request, self.session, search_term)

        filtered = False
        if '__extra_filters__' in self.model.__dict__\
        and self.model.__extra_filters__:
            for filter in self.model.__extra_filters__:
                if hasattr(self.model, filter) and filter in request.args:
                    f = getattr(self.model, filter)
                    self.query = f(request, self.query)
                    filtered = True
                    break

        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', str(conf('crud.per_page', 10)))

        offset = None
        pagination = None
        total_items = None
        if per_page and per_page != 'all':
            offset = (int(page) - 1) * int(per_page)
            items = self.query
            total_items = items.count()
            items = items.limit(per_page).offset(offset).all()
            pagination = Pagination(int(page), int(per_page), total_items)
        else:
            items = self.query.all()

        columns = self._get_model_columns(items)

        foreign_selection = False
        if 'foreign_selection' in request.args:
            foreign_selection = True

        title = self.instance_config['name']
        if self.title:
            if callable(self.title):
                title = self.title(request, *args)
            else:
                title = self.title

        subtitle = 'Listado de %s' % self.model.__verbose_name_plural__
        if self.subtitle:
            if callable(self.subtitle):
                subtitle = self.subtitle(request, *args)
            else:
                subtitle = self.subtitle

        return Template('crud_list', {
            'body_class': 'crud_list %s' % self.instance_name,
            'title': title,
            'subtitle': subtitle,
            'items': items,
            'columns': columns,
            'pagination': pagination,
            'toolbar': self.toolbar,
            'id': id,
            'current_page': int(page),
            'per_page': per_page,
            'offset': offset,
            'total_items': total_items,
            'filtered': filtered,
            'foreign_selection': foreign_selection,
            'base_url': self._url,
            'model': self.model,
            'search_term': search_term,
            'read_only': self.read_only,
            })


class CrudAdd(CrudBase):
    def __init__(self, model, query=None, template_decorator=None):
        super(CrudAdd, self).__init__(model, query=query,
            template_decorator=template_decorator)

    def __call__(self, request, *args):
        self._initialize(request, *args)

        columns = self._get_model_columns()

        item = None
        if request.method == 'POST':
            item = self._save_from_post(request, columns, self.session)
            if isinstance(item, BaseResponse):
                return item

        relations = {}
        if item and item.__load_relations_on_add__ is not None:
            for key, value in item.__load_relations_on_add__.iteritems():
                relations[key] = value(self.session, request)

        tpl_add = Template('crud_add', {
            'body_class': 'crud_add %s' % self.instance_name,
            'title': self.instance_config['name'],
            'subtitle': '%s %s' % (self.model.__verbose_name__, id),
            'columns': columns,
            'toolbar': self.toolbar,
            'item': item,
            'model': self.model,
            'base_url': self._url,
            'relations': relations,
            'session': self.session,
            'templateDecorator': self.template_decorator,
            })

        return tpl_add


class CrudUpdate(CrudBase):
    def __init__(self, model, query=None, template_decorator=None):
        super(CrudUpdate, self).__init__(model, query=query,
            template_decorator=template_decorator)

    def __call__(self, request, item_id, *args):
        self._initialize(request, *args)

        item = self.query.get(item_id)
        columns = self._get_model_columns(item)

        if request.method == 'POST':
            self._save_from_post(request, columns, self.session, item)
            if isinstance(item, BaseResponse):
                return item

        tpl_upd = Template('crud_update', {
            'body_class': 'crud_update %s' % self.instance_name,
            'title': self.instance_config['name'],
            'subtitle': '%s %s' % (
                self.model.__verbose_name__,
                item
                ),
            'columns': columns,
            'toolbar': self.toolbar,
            'item_id': item_id,
            'item': item,
            'model': self.model,
            'base_url': self._url,
            'relations': None,
            'session': self.session,
            'templateDecorator': self.template_decorator,
            })
        return tpl_upd


class CrudDelete(CrudBase):
    def __init__(self, model, query=None):
        super(CrudDelete, self).__init__(model, query=query)

    def __call__(self, request, item_id, *args):
        self._initialize(request, *args)

        item = self.query.get(item_id)

        if request.method == 'POST' and request.form.get('submit'):
            self.session.begin()
            try:
                self.session.delete(item)
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                flash(request, 'notice',
                    'No se pudo borrar el %s %s, mas elementos dependen de el!'
                    % (item.__verbose_name__, unicode(item))
                )
            else:
                return redirect('%s/../../../list' % request.base_url)

        return Template('crud_delete', {
            'body_class': 'crud_delete %s' % self.instance_name,
            'title': self.instance_config['name'],
            'subtitle': '%s %s' % (self.model.__verbose_name__, item_id),
            'toolbar': self.toolbar,
            'item_id': item_id,
            'item': item,
            'base_url': self._url,
            })


class CrudShow(CrudBase):
    def __init__(self, model, query=None, read_only=False):
        super(CrudShow, self).__init__(model, query=query)
        self.read_only = read_only

    def __call__(self, request, item_id, *args):
        self._initialize(request, *args)

        item = self.query.get(item_id)
        columns = self._get_model_columns(item)

        return Template('crud_show', {
            'body_class': 'crud_show %s' % self.instance_name,
            'title': self.instance_config['name'],
            'subtitle': '%s %s' % (self.model.__verbose_name__, item),
            'item': item,
            'columns': columns,
            'toolbar': self.toolbar,
            'id': item_id,
            'base_url': self._url,
            'read_only': self.read_only,
            })


def get_item_primary_key(item, columns):
    primary_key = None
    for column in columns:
        if column.primary_key:
            primary_key = column.key
            break

    if primary_key:
        try:
            primary_key = getattr(item, primary_key)
        except AttributeError:
            return None

    return primary_key


def get_column_data(item, column, crud_type='list'):
    icon, item_data, link = '', None, None

    try:
        item.__dict__[column.key]
    except KeyError:
        return None, None, None

    if column.foreign_keys:
        if column.name.endswith('_id'):
            relation = column.name.replace('_id', '')
            if hasattr(item, relation):
                relation_column = getattr(item, relation)
                if relation_column:
                    item_data = relation_column
                    link_dir = '../../'
                    if crud_type == 'show':
                        link_dir = '../../../'
                    link = '%s%s/show/%s' % (
                        link_dir, relation_column.__tablename__,
                        item.__dict__[column.key])

    if column.primary_key and len(item.__table__.primary_key.columns) == 1:
        item_data = item.__dict__[column.key]
        if crud_type != 'show':
            link = '../show/%s' % item_data

    if item_data is None:
        item_data = item.__dict__[column.key]
        if isinstance(item_data, bool) or column.name.startswith(
            'is_') or column.name.startswith('has_') or column.name.startswith(
            'allows_'):
            icon = 'icon-ok' if item_data else 'icon-remove'
            if crud_type == 'show':
                item_data = 'Si' if item_data else 'No'
            else:
                item_data = ''
        elif isinstance(item_data, basestring):
            item_data = item_data.replace('\n', '<br />')
        elif item_data is None:
            item_data = '&mdash;'

    return item_data, icon, link
