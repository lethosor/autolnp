import hashlib
import os
import threading

import autolnp.log as log
from autolnp.util import py3
if py3:
    from urllib.request import urlretrieve
    import queue
else:
    from urllib import urlretrieve
    import Queue as queue

max_threads = 4

class DownloadError(Exception): pass
class DownloadQueueError(Exception): pass

def local_path(url):
    sha1 = hashlib.sha1(url).hexdigest()
    return os.path.join('downloads', sha1[:2], sha1[2:20], url.split('/')[-1])

class Download(object):
    def __init__(self, url, callback=None):
        self.url = url
        self.callback = callback or lambda: None
        self.complete = False
        self.failures = 0
    def save_to(self, path):
        try:
            urlretrieve(self.url, path)
            self.complete = True
            self.callback()
        except Exception as e:
            log.w('Download of %s failed: %s', self.url, e)
            self.complete = False
            self.failures += 1

download_queue = queue.Queue()
class DownloadThread(threading.Thread):
    daemon = True
    def run():
        while True:
            dl = download_queue.get()
            if not isinstance(dl, Download):
                log.w('Invalid download: %r', dl)
                continue
            dest = local_path(dl.url)
            if os.path.exists(dest):
                log.i('Already exists: %s', dest)
                continue
            log.i('%s: Downloading to %s', dl.url, dest)
            dl.save_to(dest)
            log.i('%s: Download complete')

class DownloadQueue(object):
    def __init__(self):
        self.downloads = []
        self.lock = threading.Lock()
        self.count = 0
        self.complete_event = threading.Event()
        self.active = False
    def append(self, url):
        with self.lock:
            self.downloads.append(Download(url, self.on_download_complete))
            self.count += 1
    def start(self):
        self.active = True
    def wait(self):
        if not self.active:
            raise DownloadQueueError('Queue not started')
        self.complete_event.wait()
    def on_download_complete(self):
        with self.lock:
            self.count -= 1
            if self.count == 0:
                self.complete_event.set()
