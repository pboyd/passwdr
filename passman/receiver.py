import kernel

class Receiver:
    """Base class to aid classes that need to receive events.

    To use, declare an events() method which returns a list of Event classes
    which the class will handle. The define _handle_EventName methods to handle
    each event type."""
    def register(self):
        for event in self.events():
            kernel.subscribe(event, self)

    def receive_event(self, event):
        method_name = "_handle_%s" % (event.__class__.__name__)
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(event)

