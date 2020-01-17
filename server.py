#!/usr/bin/python
# -*- coding: utf-8 -*-
import ssl
from functools import wraps

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

import urls_tornado

settings = {'debug' : False}
define("port", default=5001, help="run on the given port", type=int)


class url_route(object):
    '''
    tornado路由类
    '''

    def __init__(self):
        self.url_config = urls_tornado.urls
        self.route_tables = []

    def _import_handle(self, handle_path):
        '''
        引入句柄
        '''
        mod, cls = handle_path.rsplit('.', 1)
        mod = __import__(mod, {}, {}, [''])
        cls = getattr(mod, cls)
        return cls

    def _generate_handle_table(self):
        '''
        组装路由
        '''
        for item in self.url_config:
            # try:
            if 1:
                new_url = (item[0], self._import_handle(item[1]))
                self.route_tables.append((new_url))
            try:
                pass
            except Exception as e:
                print("url_import error:{}".format(e))

    def get_all_route(self):
        '''
        路由表
        '''
        self._generate_handle_table()
        print(self.route_tables,)
        return self.route_tables


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)

    return bar


ssl.wrap_socket = sslwrap(ssl.wrap_socket)
options.parse_command_line()
application = tornado.web.Application(url_route().get_all_route(), **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(options.port)
    http_server.bind(options.port)
    http_server.start(num_processes=0)
    tornado.ioloop.IOLoop.instance().start()
