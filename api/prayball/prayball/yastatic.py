# -*- coding: utf-8 -*-
import os
from os.path import (
    normcase,
    normpath,
    join,
    isdir,
    exists,
    isabs,
    )
from zope.interface import implementer
from pkg_resources import (
    resource_exists,
    resource_filename,
    resource_isdir,
    )

from pyramid.util import action_method
from pyramid.config import Configurator
from pyramid.response import FileResponse
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.traversal import traversal_path_info
from pyramid.interfaces import IStaticURLInfo
from pyramid.httpexceptions import HTTPNotFound
from pyramid.config.views import (
    url_parse,
    StaticURLInfo,
    )
from pyramid.static import (
    static_view,
    _secure_path,  # hmm orz
    )


class ya_static_view(static_view):
    def __call__(self, context, request):
        if self.use_subpath:
            path_tuple = request.subpath
        else:
            path_tuple = traversal_path_info(request.environ['PATH_INFO'])
        if self.cachebust_match:
            path_tuple = self.cachebust_match(path_tuple)
        path = _secure_path(path_tuple)

        if path is None:
            raise HTTPNotFound('Out of bounds: %s' % request.url)

        if self.package_name:  # package resource
            resource_path = '%s/%s' % (self.docroot.rstrip('/'), path)
            if resource_isdir(self.package_name, resource_path):
                if not request.path_url.endswith('/'):
                    self.add_slash_redirect(request)
                resource_path = '%s/%s' % (resource_path.rstrip('/'), self.index)

            candidates = ('', '.html', '.htm', '/index.html', '/index.htm')
            for candidate in candidates:
                tmp_resource_path = resource_path + candidate
                if resource_exists(self.package_name, tmp_resource_path):
                    resource_path = tmp_resource_path
                    break
            else:
                raise HTTPNotFound(request.url)
            filepath = resource_filename(self.package_name, resource_path)

        else:  # filesystem file

            # os.path.normpath converts / to \ on windows
            filepath = normcase(normpath(join(self.norm_docroot, path)))
            if isdir(filepath):
                if not request.path_url.endswith('/'):
                    self.add_slash_redirect(request)
                filepath = join(filepath, self.index)
            if not exists(filepath):
                raise HTTPNotFound(request.url)

        return FileResponse(filepath, request, self.cache_max_age)


@implementer(IStaticURLInfo)
class YAStaticURLInfo(StaticURLInfo):
    def add(self, config, name, spec, **extra):
        # This feature only allows for the serving of a directory and
        # the files contained within, not of a single asset;
        # appending a slash here if the spec doesn't have one is
        # required for proper prefix matching done in ``generate``
        # (``subpath = path[len(spec):]``).
        if isabs(spec):  # FBO windows
            sep = os.sep
        else:
            sep = '/'
        if not spec.endswith(sep) and not spec.endswith(':'):
            spec = spec + sep

        # we also make sure the name ends with a slash, purely as a
        # convenience: a name that is a url is required to end in a
        # slash, so that ``urljoin(name, subpath))`` will work above
        # when the name is a URL, and it doesn't hurt things for it to
        # have a name that ends in a slash if it's used as a route
        # name instead of a URL.
        if not name.endswith('/'):
            # make sure it ends with a slash
            name = name + '/'

        if config.registry.settings.get('pyramid.prevent_cachebust'):
            cb = None
        else:
            cb = extra.pop('cachebust', None)
        if cb is True:
            cb = self._default_cachebust()
        if cb:
            def cachebust(subpath, kw):
                token = cb.token(spec + subpath)
                subpath_tuple = tuple(subpath.split('/'))
                subpath_tuple, kw = cb.pregenerate(token, subpath_tuple, kw)
                return '/'.join(subpath_tuple), kw
        else:
            cachebust = None  # oooops!!!! pyramid!!!!!

        if url_parse(name).netloc:
            # it's a URL
            # url, spec, route_name
            url = name
            route_name = None
        else:
            # it's a view name
            url = None  # oooops!!!! pyramid!!!!!
            ten_years = 10 * 365 * 24 * 60 * 60  # more or less
            default = ten_years if cb else None
            cache_max_age = extra.pop('cache_max_age', default)

            # create a view
            cb_match = getattr(cb, 'match', None)
            view = ya_static_view(spec, cache_max_age=cache_max_age,
                                  use_subpath=True, cachebust_match=cb_match)

            # Mutate extra to allow factory, etc to be passed through here.
            # Treat permission specially because we'd like to default to
            # permissiveness (see docs of config.add_static_view).
            permission = extra.pop('permission', None)
            if permission is None:
                permission = NO_PERMISSION_REQUIRED

            context = extra.pop('context', None)
            if context is None:
                context = extra.pop('for_', None)

            renderer = extra.pop('renderer', None)

            # register a route using the computed view, permission, and
            # pattern, plus any extras passed to us via add_static_view
            pattern = "%s*subpath" % name  # name already ends with slash
            if config.route_prefix:
                route_name = '__%s/%s' % (config.route_prefix, name)
            else:
                route_name = '__%s' % name
            config.add_route(route_name, pattern, **extra)
            config.add_view(
                route_name=route_name,
                view=view,
                permission=permission,
                context=context,
                renderer=renderer,
                )


class YAConfigurator(Configurator):
    @action_method
    def add_ya_static_view(self, name, path, **kw):
        spec = self._make_spec(path)
        info = self.registry.queryUtility(IStaticURLInfo, name='another')
        if info is None:
            info = YAStaticURLInfo()
            self.registry.registerUtility(info, IStaticURLInfo, name='another')
        info.add(self, name, spec, **kw)
