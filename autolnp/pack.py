import os
import autolnp
import autolnp.log as log
import autolnp.util as util

valid_platforms = ('linux', 'mac', 'windows')
def create(name, module, platforms, dest):
    platforms = list(set(platforms))
    platforms.sort()
    invalid_platforms = list(filter(lambda p: p not in valid_platforms, platforms))
    if len(invalid_platforms):
        raise ValueError('Unrecognized platforms: %s' % ', '.join(invalid_platforms))
    log.d('Creating pack %s for platforms %r', name, platforms)
    for p in platforms:
        pack_dest = os.path.join(dest, name, p)
        util.touchdir(pack_dest)
        pack = Pack(name=name, module=module, platform=p, dest=pack_dest)
        pack.build()

def df_url(version, platform):
    suffixes = {
        'windows': 'win.zip',
        'mac': 'osx.tar.bz2',
        'linux': 'linux.tar.bz2'
    }
    try:
        version = map(int, version.split('.'))
        assert len(version) == 3
    except (ValueError, AssertionError):
        raise ValueError('Invalid DF version: %s' % version)
    return 'http://www.bay12games.com/dwarves/df_%i_%i_%s' % (version[1], version[2], suffixes[platform])

class Pack(object):
    def __init__(self, name, module, platform, dest):
        self.name = name
        self.platform = platform
        self.dest = dest
        self.components = []
        self.df_version = module.df_version
        self.df_url = df_url(self.df_version, platform)
        module.require = self.add_component
        module.main()
    def add_component(self, name, version):
        comp = autolnp.component.find(name)(version=version, platform=self.platform)
        self.components.append(comp)
    def build(self):
        for c in self.components:
            log.d('url: %s', c.get_url())
