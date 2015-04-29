#! /usr/bin/env python
# -*- coding: utf-8 -*-

# stdlib
import sys
import argparse

# 3rd package
import wsgiref.simple_server
from sqlalchemy import engine_from_config

# frame work
import pyramid.paster

# my package
from .yastatic import (
    YAConfigurator,
    )
from .models import (
    DBSession,
    Base,
    )


def includeme(config):
    config.add_route('api.ping', '/api/ping')


def main(global_config, **local_config):
    """ This function returns a Pyramid WSGI application.
    """
    settings = dict(global_config)
    settings.update(local_config)

    # setup db
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # setup rooting
    static_root = settings.get('static_root', 'static')
    cache_max_age = int(settings.get('static_file_cache_max', 3600))
    config = YAConfigurator(settings=settings)

    config.include(includeme)
    config.scan()

    config.add_ya_static_view('/', static_root, cache_max_age=cache_max_age)

    # create app
    app = config.make_wsgi_app()
    return app


def setup(path, no_setup_loggin=False):
    """setup application

    :param path: config file path
    :param no_setup_loggin: do not setup loggin if no_setup_loggin is True
    :return: environment object
    """
    if not no_setup_loggin:
        pyramid.paster.setup_logging(path)
    env = pyramid.paster.bootstrap(path)
    return env


def serve_main(argv=sys.argv[1:]):
    """entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument('conf', nargs=1)
    parser.add_argument('static_root', nargs=1)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=8000, type=int)
    args = parser.parse_args(argv)

    env = setup(args.conf)
    app = main(env)
    server = wsgiref.simple_server.make_server(args.host, args.port, app)
    server.serve_forever()

if __name__ == '__main__':
    sys.exit(main({}))
