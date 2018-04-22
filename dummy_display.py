''' A dummy display module for debugging '''


class DummyDisplay(object):

    def __init__(self, enabled=True):
        self.enabled = enabled

    def printmsg(self, command, value):
        if self.enabled:
            print(("DummyDisplay {}: {}".format(command, value)))

    def brightness(self, value):
        self.printmsg("set brightness", value)

    def text(self, value):
        self.printmsg("print text", value)

    def fill(self, value):
        self.printmsg("fill text", value)

    def show(self):
        self.printmsg("show", "")