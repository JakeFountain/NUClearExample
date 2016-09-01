# from message.example import ExampleMessage
# from nuclear import on, Trigger, With
from message.example import ExampleMessage

def on(*args):
    def decorator(func):
        print(func.__name__)

        # When building
        print('on<{}>'.format(', '.join(a.dsl for a in args)))

        # When running we need to pass func to c++ land
        return func

    return decorator

# Always
# Buffer(int)
# Every(duration)
# IO?
# Last
# MainThread
# Network
# Optional
# Priority
# Shutdown
# Single
# Startup
# Sync
# TCP
# Trigger
# UDP
# With

class Trigger(object):
    def __init__(self, t):
        fqn = '.' + t.__module__ + '.' + t.__name__
        fqn = fqn.replace('.', '::')
        self.dsl = 'Trigger<{}>'.format(fqn)

class With(object):
    def __init__(self, t):
        fqn = '.' + t.__module__ + '.' + t.__name__
        fqn = fqn.replace('.', '::')
        self.dsl = 'With<{}>'.format(fqn)

class Single(object):
    def __init__(self):
        self.dsl = 'Single'
Single = Single()

class PythonExample(object):

    def __init__(self):
        self.example_callback()

    @on(Trigger(ExampleMessage), With(ExampleMessage), Single)
    def example_callback(self, data):
        print(self, data)

