"""
This file holds the glue logic and functions to
register, generate, and use C++ function calls
to access python code.
"""

#this is a global variable scoped to functions in this file only
___functionSignatures = {}

def on(*args):
    def decorator(func):
        # When building we save all signatures in the top level dictionary
        ___functionSignatures[func.__name__] = 'on<{}>'.format(', '.join(a.dsl for a in args))

        # When running we need to pass func to c++ land
        return func

    return decorator

def getBindingSignatures():
    #C++ can be generated all at once here, once the user code has been evaluated
    for k in ___functionSignatures.keys():
        print(k, "->", ___functionSignatures[k])