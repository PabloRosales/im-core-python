import os
from im.core.config import conf
from fabric.decorators import _list_annotating_decorator

from fabric.state import env

def hosts(*host_list):
    """
    Decorator defining which host or hosts to execute the wrapped function on.

	@hosts('user1@host1', 'host2', 'user2@host3')
	def my_func():
		pass

	Servers must be specified using the key in the configuration file and will
	be returned to fabric using the addr field.
    """
    return _list_annotating_decorator('hosts', parse_servers(host_list))

def roles(*role_list):
    """
    Decorator defining a list of role names, used to look up host lists.

	it updates roledefs first and then returns the decorator 
        env.roledefs.update({
            'webserver': ['www1', 'www2'],
            'dbserver': ['db1']
        })

        @roles('webserver', 'user@dbserver')
        def my_func():
            pass

    """
    host_list = []
    for role in role_list:
		host_list.append("role="+role)
    parse_servers(host_list)
	
    return _list_annotating_decorator('roles', *role_list)


def parse_servers(host_list):
	servers = []
	for query in host_list:
		user=conf("servers.user", None)
		port=conf("servers.port", None)
		if "@" in query:
			user, query = query.split("@",1)
		if ":" in query:
			query, port = query.split(":",1)
		
		if query == "all":
			for s, server in conf("servers").iteritems():
				servers.append(server_append(server['addr'], user, port))
		elif query == "none":
			pass
		elif query == "local":
			servers.append("local") # TODO: this doesn't work
		elif "=" in query:
			key, val = query.split("=",1)
			for s, server in conf("servers").iteritems():
				if server.get(key) == val:
					servers.append(server_append(server['addr'], user, port))
					if not env.roledefs.get(val):
						env.roledefs[val] = []
					env.roledefs[val].append(server['addr'])
		else:
			server = conf("servers").get(query)
			if server:
				servers.append(server_append(server['addr'], user, port))
	
	return servers

def server_append(server, user, port):
	server_string = server
	if user:
		server_string = user + "@" + server_string
	if port:
		server_string = server_string + ":" + port
	return server_string
