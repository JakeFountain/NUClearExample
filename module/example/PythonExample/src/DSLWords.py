"""
This file holds the DSL definitions for the NUClear keywords.
All keywords extend DSLWord, overriding __init__ to provide arg matching
"""

# FULL LIST OF KEYWORDS:
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

class DSLWord(object):
    def __init__(self, baseString = "KeyWord<{}>", *args):
        """
        Default initialiser for a DSLWord: we take a base string,
        followed by a bunch messageType args (this handles the multiple with case)
        """
        self.messages = args
        if len(args) == 0:
            self.dsl = baseString
        else:

            fqn = []
            for message in args:
                #this check allows nesting of DSLWords (for example Sync, Last, etc) in the decorator call
                if issubclass(message,DSLWord):
                    fqn.append(message.dsl)

                #this check allows functionality of last<>, etc
                elif type(message) is int:
                    fqn.append(str(message))

                #this implements reconstructing the message type name from the C library import
                else:
                    fqn.append('.' + message.__module__ + '.' + message.__name__)

            argList = ", ".join([message.replace('.', '::') for message in fqn])
            self.dsl = baseString.format(argList)

class Trigger(DSLWord):
    def __init__(self, arg):
        #Single arg will only match a single message type
        super().__init__('Trigger<{}>', arg)

class With(DSLWord):
    def __init__(self, *args):
        # *args matches a list of message types
        super().__init__('With<{}>', *args)

class Single(DSLWord):
    def __init__(self):
        #The lack of args means we just declare this as Single()
        super().__init__('Single')

