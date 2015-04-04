import os
import sys

def exit(msg, *args, **kwargs):
    try:
        print(msg % args)
    except TypeError:
        print(msg)
    sys.exit(kwargs.get('code', 1))

def load_source(path, name=''):
    # May break in future versions of Python
    import imp
    return imp.load_source(name, path)

def touchdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    elif not os.path.isdir(path):
        raise OSError('Exists but is not a directory: %s' % path)
