def DSLKeyword(name):

    return type(name, (), {
        '__init__': lambda self, t: self.template_args.append('O'),
        'typename': name,
        'template_args': [],
        'runtime_args': []
    })

# Decorator for creating instance variables/setting up reactor
def Reactor(reactor):

    print("Reactor Class:", reactor)

    return reactor


# Our on function that creates the binding
def on(*args):

    def decorator(func):

        print("""\
        using dsl = {dsl};
        """.format(dsl=', '.join('{name}<{targs}>'.format(name=w.typename, targs=', '.join(w.template_args)) for w in args)))

        # TODO print the dsl function binder

        print(func.__module__, func.__name__)
        ', '
        # print("On args:", func, args)
        # TODO print our actual function

        return func

    return decorator

#DSL Keywords
Always = DSLKeyword('Always')
MainThread = DSLKeyword('MainThread')
Single = DSLKeyword('Single')
Startup = DSLKeyword('Startup')
Shutdown = DSLKeyword('Shutdown')

# TAKES 1 TYPES
Sync = DSLKeyword('Sync')
Trigger = DSLKeyword('Trigger')
With = DSLKeyword('With')

# TAKES WEIRD TYPES
Buffer = DSLKeyword('Buffer')
Every = DSLKeyword('Every')
Priority = DSLKeyword('Priority')

# MODIFIERS
Last = DSLKeyword('Last')
Optional = DSLKeyword('Optional')

# TYPES THAT I DON'T KNOW IF I WANT

# IO? probably has no analouge in python
# TCP
# UDP

# Network
