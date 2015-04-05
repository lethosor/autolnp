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
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
