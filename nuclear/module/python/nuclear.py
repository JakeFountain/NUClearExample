import inspect


# A dsl keyword needs to provide NUClear dsl words
# A dsl keyword needs to provide runtime arguments (may be empty)

class DSLWord(object):
    pass

# Single type keywords

class SingleTypeDSLWord(DSLWord):

    def __init__(self, t):
        self._name = self.__class__.__name__
        self._t = t

    def template_args(self):
        return "{}<::{}::{}>".format(self._name, self._t.__module__.replace('.', '::'), self._t.__name__.replace('.', '::'))

class Trigger(SingleTypeDSLWord): pass
class With(SingleTypeDSLWord): pass
class Sync(SingleTypeDSLWord): pass

# No arg Keywords

class NoArgsDSLWord(DSLWord):
    def __init__(self):
        self._name = self.__class__.__name__

    def template_args(self):
        return self._name

class Always(NoArgsDSLWord): pass
class MainThread(NoArgsDSLWord): pass
class Single(NoArgsDSLWord): pass
class Startup(NoArgsDSLWord): pass
class Shutdown(NoArgsDSLWord): pass

# DSL modifiers

class Last(DSLWord):
    def __init__(self, dsl, count):
        self._name = self.__class__.__name__
        self._dsl = dsl
        self._count = count

    def template_args(self):
        return "{}<{}, {}>".format(self._name, self._count, self._dsl.template_args())

    def runtime_args(self):
        return self._dsl.runtime_args()

class Optional(DSLWord):
    def __init__(self, dsl):
        self._name = self.__class__.__name__
        self._dsl = dsl

    def template_args(self):
        return "{}<{}>".format(self._name, self._dsl.template_args())

    def runtime_args(self):
        return self._dsl.runtime_args()

# Weird types

class Buffer(DSLWord):
    def __init__(self, k):
        self._name = self.__class__.__name__
        self._k = k

    def template_args(self):
        return "{}<{}>".format(self._name, self._k)

class Every(DSLWord):
    pass

class Priority(object):
    class REALTIME(DSLWord):
        def template_arg(self):
            return "Priority::REALTIME"

    class HIGH(DSLWord):
        def template_arg(self):
            return "Priority::HIGH"

    class NORMAL(DSLWord):
        def template_arg(self):
            return "Priority::NORMAL"

    class LOW(DSLWord):
        def template_arg(self):
            return "Priority::LOW"

    class IDLE(DSLWord):
        def template_arg(self):
            return "Priority::IDLE"


# Type that holds a DSL function

class DSLCallback(DSLWord):

    def __init__(self, func, *dsl):
        self.func = func
        self._t_args = ", ".join(w.template_args() for w in dsl if hasattr(w, 'template_args') and w.template_args())
        self._r_args = ", ".join(w.runtime_args()  for w in dsl if hasattr(w, 'runtime_args')  and w.runtime_args())

    def template_args(self):
        return self._t_args

    def runtime_args(self):
        return self._r_args

    def function(self):
        return self.func

# Decorator for creating instance variables/setting up reactor
def Reactor(reactor):

    # Get our reactions
    reactions = inspect.getmembers(reactor, predicate=lambda x: isinstance(x, DSLCallback))

    for reaction in reactions:
        print(reaction[1].template_args())

    return reactor

# Our on function that creates the binding
def on(*args):

    def decorator(func):

        return DSLCallback(func, *args)

    return decorator


# TYPES THAT I DON'T KNOW IF I WANT

# IO? probably has no analouge in python
# TCP
# UDP

# Network
