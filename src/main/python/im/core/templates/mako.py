
from __future__ import absolute_import

import os
import logging
from mako import exceptions
from mako.lookup import TemplateLookup
from im.core.utils.path import get_project_path
from im.core.config import configs, RecursiveDict, conf


logger = logging.getLogger('im.core.templates.mako')


def set_defaults(vars):
    """Sets the default_vars from the configuration for templates, useful when
    need to execute code and a YAML file is not enough.
    """
    templates_config = configs.get('templates')
    if templates_config.get('default_vars', False):
        if hasattr(templates_config, 'update_recursive'):
            templates_config.update_recursive({
                'default_vars': vars,
            })
        else:
            templates_config.get('default_vars').update(vars)
    else:
        configs.get('templates')['default_vars'] = vars


class Template(object):
    """Mako Template Engine wrapper to allow easy rendering of templates.

    :param template_name: The name of the template without extension to be used.

    :param template_vars: A dict with vars to pass to the template context.

    :param config: Configuration dict to override default/global configuration

    :param template_lookup_class: The callable to use to search for the template.
    """

    default_configuration = RecursiveDict({
        'debug': False,
        'strict_undefined': True,
        'input_encoding': 'utf-8',
        'output_encoding': 'utf-8',
        'encoding_errors': 'ignore',
        'extension': 'mako',
        'directories': [],
        'default_vars': RecursiveDict({
            'logger': logger,
            'conf': conf,
        }),
    })

    def __init__(self, template_name, template_vars=None, config=None,
            _format='html', template_lookup_class=TemplateLookup, layout={}):

        self.config = self.default_configuration
        self.config.update_recursive(configs.get('templates', {}))
        if config:
            self.config.update_recursive(config)

        self.template_name = template_name

        # add project path templates
        project_templates = os.path.join(get_project_path(), 'templates')
        if not project_templates in self.config['directories']:
            self.config['directories'].insert(0,project_templates)
            
        template_lookup = TemplateLookup(
            directories=self.config.get('directories'),
            input_encoding=self.config.get('input_encoding'),
            output_encoding=self.config.get('output_encoding'),
            encoding_errors=self.config.get('encoding_errors'),
            strict_undefined=self.config.get('strict_undefined'),
            default_filters=self.config.get('default_filters', self.config.get('default_filters'))
        )

        self.template_format = _format

        self.template_inherit = None
        self.template_sections = None
        self.template_layout = None

        if layout:
            self.template_inherit = ".".join([layout.get("master"),layout.get("format")])
            self.template_layout = ".".join([layout.get("layout"),layout.get("format")])
            self.template_name = ".".join(["/" + self.template_name,layout.get("format")])
        else:
            self._check_for_layout()
        
        self.template = template_lookup.get_template(self.template_name)
        self.template_vars = self.config.get('default_vars')
        self.template_vars.update_recursive(template_vars or {})

        self.rendered = None

    def _check_for_layout(self):
        try:
            layout = conf('layouts.layouts.%s' % self.template_name, False)
        except AttributeError:
            layout = False
        
        if not layout:
            logger.debug('Getting template %s' % self.template_name)
            self.template_name = '%s.%s' % (self.template_name, self.config.get('extension'))
            return

        inherit = layout.get('inherit', '/core/layouts/empty')
        self.template_inherit = inherit % {'format': self.template_format}
        self.template_sections = layout.get('sections', False)
        self.template_name = '/core/layouts/%(format)s/base.%(extension)s' % {
            'format': self.template_format,
            'extension':  self.config.get('extension'),
        }
        
        self.template_layout = layout

    def render(self, vars=None, force=True):
        """Renders the template to a string, if already rendered will not render
        again unless force is set to True.

        :param force: If True then will render the template again, if False \
        will check first if its already rendered.
        """
        self.template_vars.update_recursive({
            '__inherit__': self.template_inherit,
            '__sections__': self.template_sections,
            '__format__': self.template_format,
            '__layout__': self.template_layout,
        })

        self.template_vars.update_recursive(vars or {})
        if not force and self.rendered is not None:
            return self.rendered
        else:
            try:
                output = self.template.render_unicode(**self.template_vars)
            except Exception, e:
                if self.config.get('debug'):
                    output = exceptions.html_error_template().render()
                else:
                    logger.error(exceptions.text_error_template().render())
                    raise Exception(e)
        self.rendered = output
        return output

    def __unicode__(self):
        return self.render_unicode()

    def __str__(self):
        return self.render()
