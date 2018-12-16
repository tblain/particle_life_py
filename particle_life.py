from tkinter import *
import time
import numpy as np
import math
import random
from math import hypot

root = Tk()
canv = Canvas(root, highlightthickness=5)
canv.pack(fill='both', expand=True)
root.geometry('%sx%s+%s+%s' %(640, 480, 100, 100))

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

class Type:
    name = ""
    relations = {}

    def __init__(self, id, name, relations):
        self.id = id
        self.name = name
        self.relations = relations

blue = Type('b', "blue", {'b' : 4, 'r' : -3, 'g' : -1, 'y' : -1, 'p' : 3, 'o' : -2})
red = Type('r', "red", {'b' : 1, 'r' : -2, 'g' : -2, 'y' : 4, 'p' : 2, 'o' : 2})
green = Type('g', "green", {'b' : -3, 'r' : 2, 'g' : 1, 'y' : 1, 'p' : 4, 'o' : -2})
yellow = Type('y', "yellow", {'b' : -2, 'r' : 4, 'g' : -3, 'y' : 2, 'p' : -4, 'o' : 3})
purple = Type('p', "purple", {'b' : 2, 'r' : 3, 'g' : -3, 'y' : -4, 'p' : 3, 'o' : -2})
orange = Type('o', "orange", {'b' : -1, 'r' : 4, 'g' : -4, 'y' : -2, 'p' : 3, 'o' : -4})

def distance(p1, p2):
     return math.hypot(p1.x - p2.x, p1.y - p2.y)

def distancexy(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

class Particle:
    """docstring for Particle."""
    op = []
    def __init__(self, type, x, y, radius):
        self.type = type
        self.x = x
        self.y = y
        self.r = radius
        self.b = canv.create_circle(x, y, radius, fill=type.name)
        self.v = [0, 0]

    def set_other_particles(self, other_particles):
        self.op = other_particles.copy()
        self.op.remove(self)

    def calculate_vector(self):
        self.v[0] = 0
        self.v[1] = 0
        # print("\n" + str(self.type))
        # print("fdsfsdfsdf" + str(self.v))
        for p in self.op:
            di = max(distance(self, p), 1)
            # print("di " + str(di))
            dx = p.x - self.x
            dy = p.y - self.y
            # di = max(math.sqrt(dx*dx + dy*dy), 1)

            poids = self.type.relations[p.type.id]

            # print("dx:" + str(round(dx * (poids/di))) + " | dy:" + str(round(dy * (poids/di))))

            self.v[0] += round(dx * ( 20 * poids / (di**2) ))
            self.v[1] += round(dy * ( 20 * poids / (di**2) ))

            if(distancexy(self.x + self.v[0], self.y, p.x, p.y) < max(self.r, p.r)):
                self.v[0] = 0

            if(distancexy(self.x, self.y + self.v[1], p.x, p.y) < min(self.r, p.r)):
                self.v[1] = 0

            # print("dx " + str(dx) + " dy " + str(dy))
        # print("c " + str(self.v))

    def move(self, can):
        # print("m " + str(self.v))
        x = self.x + self.v[0]
        y = self.y + self.v[1]

        x = max(self.r, x)
        y = max(self.r, y)

        x = min(600 - self.r, x)
        y = min(600 - self.r, y)

        # print("x " + str(x) + " y " + str(y))
        # print("sx " + str(self.x) + " sy " + str(self.y))
        # print("v " + str(self.v[0]) + " " + str(self.v[1]))

        diffx = x - self.x
        diffy = y - self.y

        self.x = x
        self.y = y

        # print("diff " + str(diffx) + " " + str(diffy))
        can.move(self.b, diffx, diffy)

list_particle = []

for i in range(1, 20):
    list_particle.append(Particle(blue, random.randrange(20, 580), random.randrange(20, 580), 10))
    list_particle.append(Particle(red, random.randrange(20, 580), random.randrange(20, 580), 10))
    list_particle.append(Particle(green, random.randrange(20, 580), random.randrange(20, 580), 10))
    list_particle.append(Particle(yellow, random.randrange(20, 580), random.randrange(20, 580), 10))
    list_particle.append(Particle(purple, random.randrange(20, 580), random.randrange(20, 580), 10))
    list_particle.append(Particle(orange, random.randrange(20, 580), random.randrange(20, 580), 10))

for p in list_particle:
    p.set_other_particles(list_particle)

while True:
    for p in list_particle:
        p.calculate_vector()

    for p in list_particle:
        p.move(canv)

    time.sleep(0.001)
    canv.update()


root.mainloop()
