import inspect
import json

import autolnp

class ComponentError(Exception): pass

def find(name):
    path = 'components/%s.py' % name
    try:
        module = autolnp.util.load_source(path)
        candidates = filter(lambda v: issubclass(v, Component) and v is not Component,
                        filter(lambda v: inspect.isclass(v),
                            map(lambda k: getattr(module, k),
                                dir(module))))
        if len(candidates) != 1:
            raise ComponentError('Expected 1 component in %s, found %i' %
                (path, len(candidates)))
        cls = candidates[0]
        cls.name = name
        return cls
    except ImportError:
        raise ComponentError('Component not found: %s (%s)' % (name, path))

class Component(object):
    def __init__(self, version=None, platform=None):
        self.version, self.platform = version, platform
        if not hasattr(self, 'name'):
            raise ValueError('%s.name is not defined' % self.__class__.__name__)
    def get_url(self, version=None, platform=None):
        if version is None: version = self.version
        if platform is None: platform = self.platform
        with open('components/%s.json' % self.name) as f:
            contents = json.load(f)
            if not version in contents:
                raise ValueError('No URL specified for version %s of %s' %
                    (version, self.name))
            if not platform in contents[version]:
                raise ValueError('Version %s of %s not available on platform: %s' %
                    (version, self.name, platform))
            return contents[version][platform]
    def install(self, src, dest):
        raise NotImplementedError
