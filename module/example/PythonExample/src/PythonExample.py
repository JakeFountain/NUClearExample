#!/usr/bin/env python3

from message.example import ExampleMessage, PythonResponse
from nuclear import Reactor, on, Trigger, Single, With

@Reactor
class PythonExample(object):

    def __init__(self):
        print("Constructing PythonExample in python")

    @on(Trigger(ExampleMessage), With(ExampleMessage), Single())
    def example_callback(self, trigger_data, with_data):
        print(self, trigger_data.timestamp, with_data.timestamp)

        msg = PythonResponse('sup c++')

        self.emit(msg)
