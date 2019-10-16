'''
Description:
    Definition of shapes class and sup classes

Information on authors:
    Name:                           Contribution:
    ---------                       ------------------
    Jacob                           Original code
    Kristinn Hlidar Gretarsson      Original code


Version history:

'''

# Import
from math import sqrt

# Definitions
class Shapes(object):
    def __init__(self):
        self.name = 'I\'m just a blob'
        self.h = 0
        self.b = 0

    def changeShape(self, new_shape):
        shapes = ['rectangle', 'triangle', 'circle']
        if new_shape.lower() in shapes:
            self.name = new_shape.lower()

    def giveParameters(self):
        return print(self.parameter())

    def parameter(self):
        return 'I\'m just a blob'

    def changeParameter(self):
        print('I don\'t know how to do that')

    def width(self, location):
        return 0

    def getWidth(self, location):
        return self.width(location)

    def getHeight(self):
        return self.h

    def isValidShapeParameter(self, input):
        if type(input) == float:
            return True
        else:
            print(f'{input} is not valid input into {self}')

    def __str__(self):
        return self.name




class Rectangle(Shapes):
    def __init__(self, breadth=0., height=0.):
        self.name = 'rectangle'
        self.b = breadth
        self.h = height

    def parameter(self):
        return f'{self.name} width = {self.b} and height = {self.h}'

    def width(self, location):
        if location <= self.h:
            return self.b
        else:
            print(f'location is outside of shape with height {self.h}')

    def changeParameter(self, breadth=0., height=0.):
        if breadth:
            self.b = breadth
        if height:
            self.h = height


class Triangle(Shapes):
    def __init__(self, breadth=0., height=0.):
        self.name = 'triangle'
        self.b = breadth
        self.h = height

    def parameter(self):
        return f'{self.name} width = {self.b} and height = {self.h}'

    def width(self, location):
        if location <= self.h:
            b = self.b * location / self.h
            return b
        else:
            print(f'location is outside of shape with height {self.h}')

    def changeParameter(self, breadth=0., height=0.):
        if breadth:
            self.b = breadth
        if height:
            self.h = height


class Circle(Shapes):
    def __init__(self, diameter=0):
        self.name = 'circle'
        self.d = diameter

    def width(self, location):
        if location <= self.d:
            b = 2 * sqrt(2 * location * self.d / 2 - location * location)
            return b
        else:
            print(f'location is outside of circle with diameter {self.d}')

    def changeParameter(self, diameter=0):
        if diameter:
            self.d = diameter

    def getHeight(self):
        return self.d


class T_beam(Shapes):
    def __init__(self, breadth=0, height=0, flange_breadth=0, flange_height=0):
        self.name = 'T-beam'
        self.b = breadth
        self.h = height
        self.f_b = flange_breadth
        self.f_h = flange_height

    def width(self, location):
        if 0 <= location <= self.f_h:
            b = self.f_b
            return b
        elif self.f_h < location <= self.h:
            b = self.b
            return b
        else:
            print(f'location {location} is outside of shape T-beam')

    def changeParameter(self, breadth=0, height=0, flange_breadth=0, flange_height=0):
        if breadth:
            self.b = breadth
        if height:
            self.h = height
        if flange_breadth:
            self.f_b = flange_breadth
        if flange_height:
            self.f_h = flange_height


class I_beam(Shapes):
    def __init__(self, breadth=0, height=0, flange_u_breadth=0, flange_u_height=0,
                 flange_l_breadth=0, flange_l_height=0):
        self.name = 'I-beam'
        self.b = breadth
        self.h = height
        self.fu_b = flange_u_breadth
        self.fu_h = flange_u_height
        self.fl_b = flange_l_breadth
        self.fl_h = flange_l_height

    def width(self, location):
        if 0 <= location <= self.fu_h:
            return self.fu_b
        elif self.fu_h < location <= self.h - self.fl_h:
            return self.b
        elif self.h - self.fl_h < location <= self.h:
            return  self.fl_b
        else:
            print(f'Location {location} is outside of shape I-beam')

    def changeParameter(self, breadth=0, height=0, flange_u_breadth=0, flange_u_height=0,
                 flange_l_breadth=0, flange_l_height=0):
        if breadth:
            self.b = breadth
        if height:
            self.h = height
        if flange_u_breadth:
            self.fu_b = flange_u_breadth
        if flange_u_height:
            self.fu_h = flange_u_height
        if flange_l_breadth:
            self.fl_b = flange_l_breadth
        if flange_l_height:
            self.fl_h = flange_l_height


# Run main program
if __name__ == '__main__':
    a = Rectangle(16, 28)

    print(a.getHeight())

    test = isinstance(a, Shapes)

    a.changeParameter(16., 28.)

    a.giveParameters()

    print(test)
