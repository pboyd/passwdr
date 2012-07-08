from Queue import Queue
from threading import Thread

_events = {}
_queue = Queue()

def subscribe(event_type, handler):
    key = event_type.__name__

    if not key in _events:
        _events[key] = []

    _events[key].append(handler)

def queue(event):
    _queue.put(event)

def join():
    _queue.join()

def _worker():
    while True:
        event = _queue.get()
        event_type = event.__class__.__name__

        if event_type in _events:
            for handler in _events[event_type]:
                handler.receive_event(event)

        _queue.task_done()

def run():
    t = Thread(target=_worker)
    t.daemon = True
    t.start()

