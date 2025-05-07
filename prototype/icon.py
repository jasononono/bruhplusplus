import pygame as p

class Instruction:
    def __init__(self):
        self.template = []

    def draw_line(self, start, end):
        self.template.append((Icon.draw_line, (start, end)))

class Icon:
    def __init__(self, instruction, size = (19, 19), colour = (69, 69, 79)):
        self.size = size
        self.instruction = instruction
        self.colour = colour

    def display(self, screen, position = (0, 0)):
        for i, j in self.instruction.template:
            i(self, screen.surface, position, *j)

    def draw_line(self, surface, position, start, end):
        p.draw.line(surface, self.colour,
                    [position[0] + start[i] * self.size[i] for i in range(2)],
                    [position[1] + end[i] * self.size[i] for i in range(2)], 2)

x = Instruction()
x.draw_line((0.3, 0.3), (0.7, 0.7))
x.draw_line((0.3, 0.7), (0.7, 0.3))