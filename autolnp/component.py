import json

class Component(object):
    def __init__(self):
        super(Component, self).__init__()
        if not hasattr(self, name):
            raise ValueError('%s.name is not defined' % self.__class__.__name__)
    def get_url(self, version, platform):
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
