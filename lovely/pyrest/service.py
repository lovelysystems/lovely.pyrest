# Shared Source Software
# Copyright (c) 2013 Lovely Systems GmbH

import venusian
import functools


METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PURGE']

DEFAULTS = {
    'renderer': 'json'
}


class Service(object):

    def __init__(self, name, path, description=None, depth=1, **kw):
        self.name = name
        self.path = path
        self.description = description
        self.definitions = []
        self.methods = []

        # this callback gets called when config.scan() gets triggered
        # and registers the service itself
        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_service(self)
        # attach the callback to venusian so it gets called at scan
        info = venusian.attach(self, callback, category='pyramid', depth=depth)

        # add aliases for the decorators
        for m in METHODS:
            setattr(self, m.lower(),
                    functools.partial(self.decorator, m))

    # The decorator to add a view to a service
    def decorator(self, method, **kwargs):
        def wrapper(view):
            self.add_view(method, view, **kwargs)
            return view
        return wrapper

    def add_view(self, method, view, **kwargs):
        method = method.upper()
        args = self.get_args(kwargs)

        self.definitions.append((method, view, args))
        if method not in self.methods:
            self.methods.append(method)

    def content_types(self, method):
        types = []
        for m, v, args in self.definitions:
            if m == method and 'content_type' in args:
                types.append(args['content_type'])
        return types

    def acceptables(self, method):
        acceptable = []
        for m, v, args in self.definitions:
            if m == method and 'accept' in args:
                acceptable.append(args['accept'])
        return acceptable

    def get_args(self, args=None):
        if args is None:
            args = {}
        arguments = {}

        for arg in DEFAULTS:
            # get the value from the passed conf
            # then from the DEFAULTS
            arguments[arg] = args.get(arg, DEFAULTS[arg])
        # update the defaults with the passed args
        arguments.update(args)
        return arguments