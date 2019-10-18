'''
Description:
    Definition of cross section class

Information on authors:
    Name:                           Contribution:
    ---------                       ------------------
    Jacob                           Original code
    Kristinn Hlidar Gretarsson      Original code


Version history:

'''

# Import
from math import sqrt
import matplotlib.pyplot as plt
from numpy import array, linspace, zeros_like

# Import our creations
from Shapes import *
from Steel import *
from Concrete import *

# Definitions
class CrossSection(object):
    def __init__(self):
        self.steel_list = []
        self.shape = Rectangle(10., 10.)
        self.concrete = Concrete()


    def addSteel(self, S):
        if isinstance(S, Steel):
            if S.getLocation() in self.steelLocations() and S.getLocation() < self.shape.getHeight():
                print(f'use modify if you want to modify steel at loaction {i.getLocation()}')
            elif S.getLocation() > self.shape.getHeight():
                print(f'Steel cannot be placed outside of cross section shape')
            else:
                self.steel_list.append(S)



    # Returns a list with steel locations in the cross section
    def steelLocations(self):
        locations = []
        for i in self.steel_list:
            locations.append(i.getLocation())
        return locations


    def printSteelInfo(self):
        for i in self.steel_list:
            location = i.getLocation()
            amount = i.getAmount()
            bar_type = i.getBarType()

            print(f'{amount} bars of {bar_type} at location {location}')


    def changeShape(self, shape):
        if isinstance(shape, Shapes):
            self.shape = shape
        else:
            print(f'{shape} is not a valid shape')

    def changeConcrete(self, new_concrete):
        if isinstance(new_concrete, Concrete):
            self.concrete = new_concrete
        else:
            print(f'{type(new_concrete)} is not a concrete type')



    def getConcreteForce(self, strain, location, neutral_axis):
        layers =  200
        spacing = 0.5 / layers
        y = linspace(self.shape.getHeight() * spacing , self.shape.getHeight() * (1 - spacing), layers - 1)
        curv = strain / (neutral_axis - location)


        h = self.shape.getHeight() / layers

        force = 0

        for i in y:
            e = curv * (neutral_axis - i)
            stress = self.concrete.getStress(e)
            b = self.shape.getWidth(i)

            force = force + stress * b * h

        return force

    def getSteelForce(self, strain, location, neutral_axis):
        curve = strain / (neutral_axis - location)

        force = 0

        for steel in self.steel_list:
            e = curve * (neutral_axis - steel.getLocation())
            force = force + steel.force(e)

            if e < self.concrete.getRuptureStrain():
                f = self.concrete.getStress(e)
                force = force - f * steel.getStealArea()


        return force

    def getTotalForce(self, strain, location, neutral_axis):
        forceConcrete = self.getConcreteForce(strain, location, neutral_axis)

        forceSteel = self.getSteelForce(strain, location, neutral_axis)

        force = forceConcrete + forceSteel

        return force

    def findNeutralAxis(self, strain, location):
        guess1 = self.shape.getHeight() / 2 - self.shape.getHeight() / 20
        guess2 = self.shape.getHeight() / 2 + self.shape.getHeight() / 20


        #step = self.shape.getHeight() / 10
        #slope = 0
        #stepsize = 1
        counter = 1

        force1 = self.getTotalForce(strain, location, guess1)
        force2 = self.getTotalForce(strain, location, guess2)
        error = abs(force1)

        while error > 0.00001:

            slope1 = (force2 - force1) / (guess2 - guess1)
            step1 = + force2 / slope1
            guess1 = guess2 - force2 / slope1
            guess1 = guess2 - step1 * 3 / 4
            force1 = self.getTotalForce(strain, location, guess1)

            slope2 = (force1 - force2) / (guess1 - guess2)
            step2 = force1 / slope2
            guess2 = guess1 - force1 / slope2
            guess2 = guess1 - step2 * 3 / 4
            force2 = self.getTotalForce(strain, location, guess2)

            #if (force1 < 0 and force2 > 0) or (force1 > 0 and force2 < 0):
             #   stepsize = stepsize + 1

            #if force1 > 0.:
            #    guess = min(guess + step / pow(2, stepsize), self.shape.getHeight())
            #else:
            #    guess = max(guess - step / pow(2, stepsize), 0)


            #force2 = force1
            error = abs(force2)
            counter += 1
            if counter > 100:
                print(f'{error} after 100 tries... get better code')
                break
        #print(f'error is {error} in {counter} iterations')
        return guess2

    def findMomentTotal(self, strain, location, neutral_axis=0):
        if neutral_axis:
            c = neutral_axis
        else:
            c = self.findNeutralAxis(strain, location)

        moment_concrete = self.findMomentConcrete(strain, location, c)
        moment_steel = self.findMomentSteel(strain, location, c)

        moment = moment_concrete + moment_steel

        return moment

    def findMomentConcrete(self, strain, location, neutral_axis):
        layers = 100
        spacing = 0.5 / layers
        y = linspace(self.shape.getHeight() * spacing, self.shape.getHeight() * (1 - spacing), layers - 1)
        curv = strain / (neutral_axis - location)

        h = self.shape.getHeight() / layers

        moment = 0

        for i in y:
            e = curv * (neutral_axis - i)
            stress = self.concrete.getStress(e)
            b = self.shape.getWidth(i)

            moment = moment + stress * b * h * (i - neutral_axis)

        return moment

    def findMomentSteel(self, strain, location, neutral_axis):
        curve = strain / (neutral_axis - location)

        moment = 0

        for steel in self.steel_list:
            e = curve * (neutral_axis - steel.getLocation())

            moment = moment + steel.force(e) * (steel.getLocation() - neutral_axis)
        return moment



    def PlotConcreteStress(self, strain, location):
        neutral_axis = self.findNeutralAxis(strain, location)

        y = linspace(0, self.shape.getHeight(), 100)
        x = zeros_like(y)

        curve = strain / (neutral_axis - location)
        e = curve * (neutral_axis - y)


        for i in range(y.size):
            x[i] = self.findMomentTotal(strain[i], location)


        plt.plot(x, -y, '-b')
        plt.grid(True)
        plt.xlabel('stress')
        plt.ylabel('y')
        plt.show()

    def PlotMomentCurve(self, scale='kip*ft'):
        strain_0 = 0
        strain_1 = -0.0038
        location = 0

        steps = 100

        strain = linspace(strain_0, strain_1, steps)

        stress = zeros_like(strain)
        curve = zeros_like(strain)

        for i in range(strain.size):
            neutral_axis = self.findNeutralAxis(strain[i], location)
            stress[i] = self.findMomentTotal(strain[i], location, neutral_axis)
            curve[i] = strain[i] / (neutral_axis - location)

        if scale == 'kip*ft':
            stress = stress / 12

        plt.plot(curve, stress, '-b')
        plt.grid(True)
        plt.xlabel('curve')
        plt.ylabel('stress')
        plt.show()

    def PlotStressInCrossSection(self, strain, location, neutral_axis=0):
        '''
        Plots stress in cross section for given strain and location, and optional neutral axis.
            If neutral axis is not specified it is calculated automatically.
        :param strain:              Strain at location
        :param location:            Location of strain
        :param neutral_axis:        Location of neutral axis
        :return:                    Nothing, plots stress over cross section
        '''

        if neutral_axis:
            c = neutral_axis
        else:
            c = self.findNeutralAxis(strain, location)

        y = linspace(0, self.shape.getHeight(), 100)
        stress_c = zeros_like(y)

        curve = strain / (neutral_axis - location)
        e = curve * (neutral_axis - y)

        for i in range(y.size):
            stress_c[i] = self.concrete.getStress(e[i])


        plt.plot(stress_c, -y, '-b')
        plt.grid(True)
        plt.xlabel('stress')
        plt.ylabel('y')
        plt.show()








# Run main program
if __name__ == '__main__':

    # Crate the shape of the cross section
    shape = Rectangle(16., 28.)
    #shape = Triangle(16., 28.)
    #shape = Circle(28.)
    #shape = T_beam(16, 28, 30, 8)

    # Create the steel that goes into the cross section
    steel1 = Steel(5, '#9', 26)
    steel1.changeGrade('60GR')
    steel2 = Steel(0, '#4', 2)
    print(steel1.getAmount())

    # Create the cross section
    cross_section = CrossSection()

    # Update shape of cross section
    cross_section.changeShape(shape)

    # Add steel to the cross section
    cross_section.addSteel(steel1)
    cross_section.addSteel(steel2)


    # Assignment 4
    # Problem 1
    cross_section.PlotMomentCurve()

    # i)
    M = cross_section.findMomentTotal(131e-6, 28) / 12
    print(f'Moment at cracking is {M} kip * ft')

    # ii) Need to find a solution for this


    # iii)
    M = cross_section.findMomentTotal(steel1.grade.strain_y(), steel1.getLocation()) / 12
    print(f'Moment at yield is {M} kip * ft')

    # iv)
    M = cross_section.findMomentTotal(-0.0025, 0) / 12
    print(f'Moment at strain of -0.0025 is {M} kip * ft')

    # v)
    M = cross_section.findMomentTotal(-0.003, 0) / 12
    print(f'Moment at strain of -0.003 is {M} kip * ft')

    # vi)
    M = cross_section.findMomentTotal(-0.0038, 0) / 12
    print(f'Moment at strain of -0.0038 is {M} kip * ft')


    # Problem 2

    # Changing the shape to a circle
    shape = Circle(28)

    # Change steel in cross section
    steel1.setSteelInfo('#10', 2, 8.3175)
    steel2.setSteelInfo('#10', 2, 14)
    steel2.changeGrade('60GR')

    # Create new layer of steel and add it
    steel3 = Steel(2, '#10', 19.6825)
    steel3.changeGrade('60GR')
    cross_section.addSteel(steel3)

    # Create moment curvature
    cross_section.PlotMomentCurve()

    # i)
    M = cross_section.findMomentTotal(131e-6, 28) / 12
    print(f'Moment at cracking is {M} kip * ft')

    # ii)
    M = cross_section.findMomentTotal(steel3.grade.strain_y(), steel3.getLocation()) / 12
    print(f'Moment at yield is {M} kip * ft')

    # ii)
    M = cross_section.findMomentTotal(-0.0025, 0) / 12
    print(f'Moment at strain of -0.0025 is {M} kip * ft')

    # iv)
    M = cross_section.findMomentTotal(-0.003, 0) / 12
    print(f'Moment at strain of -0.003 is {M} kip * ft')

    # v)
    M = cross_section.findMomentTotal(-0.0038, 0) / 12
    print(f'Moment at strain of -0.0038 is {M} kip * ft')










