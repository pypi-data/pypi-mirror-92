# Super small event helper
class Event:
    def __init__(self):
        self.subscribedListeners = []
    def __call__(self, *args):
        for listener in self.subscribedListeners:
            listener()
    def __iadd__(self, method):
        self.subscribedListeners.append(method)
        return self
    def __isub__(self, method):
        if method in self.subscribedListeners:
            self.subscribedListeners.remove(method)
        return self
