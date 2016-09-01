# from message.example import ExampleMessage
# from nuclear import on, Trigger, With
from message.example import ExampleMessage
from DSLWords import *
from NUClearBinding import on, getBindingSignatures

class PythonExample(object):

    def __init__(self):
        self.example_callback()

    @on(Trigger(ExampleMessage), With(ExampleMessage), Single())
    def example_callback(self, data):
        print(self, data)

getBindingSignatures()