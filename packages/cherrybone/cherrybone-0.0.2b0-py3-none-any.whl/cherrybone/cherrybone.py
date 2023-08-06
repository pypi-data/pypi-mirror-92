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
    def __init__(self,
                 app,
                 port=None,
                 path=None,
                 host=None,
                 threads=None,
                 max_body_bytes=None,
                 max_header_bytes=None,
                 max_threads=None,
                 max_queued_connection=None,
                 connection_timeout=None,
                 max_queued_requests=None,
                 request_acceptance_timeout=None,
                 tcp_nodelay=None,
                 shutdown_timeout=None):
        self._app = app
        self._path = '/' if not path else path

        port = 80 if not port else port
        host = '0.0.0.0' if not host else host
        threads = multiprocessing.cpu_count() if not threads else threads
        max_body_bytes = 1073741824 if not max_body_bytes else max_body_bytes  # 1 GiB
        max_header_bytes = 1048576 if not max_header_bytes else max_header_bytes  # 1 MiB
        max_threads = -1 if not max_threads else max_threads
        max_queued_connection = 10 if not max_queued_connection else max_queued_connection
        connection_timeout = 10 if not connection_timeout else connection_timeout
        max_queued_requests = -1 if not max_queued_requests else max_queued_requests
        request_acceptance_timeout = 10 if not request_acceptance_timeout else request_acceptance_timeout
        tcp_nodelay = False if not tcp_nodelay else True
        shutdown_timeout = 10 if not shutdown_timeout else shutdown_timeout

        cherrypy.config.update({
            'server.socket_port': port,
            'server.socket_host': host,
            'server.thread_pool': threads,
            'server.thread_pool_max': max_threads,
            'server.max_request_body_size': max_body_bytes,
            'server.max_request_header_size': max_header_bytes,
            'server.socket_queue_size': max_queued_connection,
            'server.socket_timeout': connection_timeout,
            'server.accepted_queue_size': max_queued_requests,
            'server.accepted_queue_timeout': request_acceptance_timeout,
            'server.nodelay': tcp_nodelay,
            'server.shutdown_timeout': shutdown_timeout,
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
