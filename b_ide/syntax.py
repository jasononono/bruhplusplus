class Syntax:
    def __init__(self, name):
        self.name = name

        self.functions = []
        self.keywords = []

    def define(self, name):
        self.functions.append(name)

    def assign(self, name):
        self.keywords.append(name)

syntax = Syntax(self, "Bruh++ Version 0.1")
