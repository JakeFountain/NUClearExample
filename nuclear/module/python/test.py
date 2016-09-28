#!/usr/bin/env python3
from nuclear import Reactor, on, Trigger, Single, With, Priority

class P(object):
    pass

@Reactor
class PythonExample(object):

    @on(Trigger(Trigger), With(P), Priority.HIGH())
    def an_example_function(self, p):
        print(p)

    @on(Trigger(Trigger), Single(), Priority.HIGH())
    def an_example_function2(self, p):
        print(p)
