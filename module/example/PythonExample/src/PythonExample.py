#!/usr/bin/env python3

from message.example import ExampleMessage
from nuclear import Reactor, on, Trigger, Single, With

@Reactor
class PythonExample(object):

    def __init__(self):
        self.example_callback()

    @on(Trigger(ExampleMessage), With(ExampleMessage), Single())
    def example_callback(self, data):
        print(self, data)
