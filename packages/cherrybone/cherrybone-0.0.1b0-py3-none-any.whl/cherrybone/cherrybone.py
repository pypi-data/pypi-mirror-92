#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon
import logging
import cherrypy
import multiprocessing

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Server:
    def __init__(self, app, port=None, path=None, interface=None, threads=None):
        self._app = app
        self._path = '/' if not path else path

        port = 80 if not port else port
        interface = '0.0.0.0' if not interface else interface
        threads = multiprocessing.cpu_count() if not threads else threads

        cherrypy.config.update({
            'server.socket_port': port,
            'server.socket_host': interface,
            'server.thread_pool': threads,
            'engine.autoreload.on': False,
            'checker.on': False,
            'tools.log_headers.on': False,
            'request.show_tracebacks': False,
            'request.show_mismatched_params': False,
            'log.screen': False,
            'engine.SIGHUP': None,
            'engine.SIGTERM': None
        })

    def start(self):
        cherrypy.tree.graft(self._app, self._path)
        cherrypy.engine.start()

    def stop(self):
        cherrypy.engine.exit()
