import sys
import threading

class Logger(object):
    locks = {}
    def __init__(self, enabled=True, fd=sys.stdout):
        self.enabled = enabled
        self.fd = fd
        self.locks.setdefault(fd, threading.Lock())
    def __call__(self, *args, **kwargs):
        if not self.enabled:
            return
        try:
            msg = args[0] % args[1:]
        except TypeError:
            msg = ' '.join(args)
        if kwargs.get('newline', True) and not msg.endswith('\n'):
            msg += '\n'
        elif not kwargs.get('newline', True):
            msg = msg.rstrip('\n')
        with self.locks[self.fd]:
            self.fd.write(msg)
            if kwargs.get('flush', True):
                self.fd.flush()

debug = d = Logger(enabled=False)
info = i = Logger()
warning = warn = w = Logger(fd=sys.stderr)
