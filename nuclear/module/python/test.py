#!/usr/bin/env python3
from nuclear import Reactor, on, Trigger

class P(object):
    pass

@Reactor
class PythonExample(object):

    @on(Trigger(P))
    def an_example_function(self, p):
        print(p)
