import os
from django.core.wsgi import get_wsgi_application
from im.core.config import configs, conf

class Application():

	def init(self):
		self.application = get_wsgi_application()

	def register_templates(self):
		if configs.get('templates') is None:
			configs['templates'] = {}

		if configs['templates'].get('directories') is None:
			configs['templates']['directories'] = []

		app_templates = os.path.join(conf('project_path'), 'templates')
		configs['templates']['directories'].append(app_templates)

	def register_queries(self):
		if configs.get('queries') is None:
			configs['queries'] = {}

		if configs['queries'].get('query_directories') is None:
			configs['queries']['query_directories'] = []

		app_templates = os.path.join(conf('project_path'), 'queries')
		configs['queries']['query_directories'].append(app_templates)

application = Application()