'''
Description:
    Definition of concrete class

Information on authors:
    Name:                           Contribution:
    ---------                       ------------------
    Jacob                           Original code
    Kristinn Hlidar Gretarsson      Original code


Version history:

'''

# Import
import matplotlib.pyplot as plt
from numpy import array, linspace, zeros_like

from math import sqrt

# Definitions



class Concrete(object):
    def __init__(self):
        self.name = '4000'
        self.fc = 0
        self.e_ult = 0.
        self.stress_strain_m = 'hognestad'
        self.strengthInfo()


    def changeClass(self, new_class):
        pass

    def changeStressStrainMethod(self, new_method):
        methods = ('hognestad', 'linear')
        if new_method in methods:
            self.stress_strain_m = new_method

    def strengthInfo(self, info=''):
        properties = {'4000': {"f'c": -4000, 'e_ult': -0.0038},
                      '6000': {"f'c": -6000, 'e_ult': -0.0038}}
        if info == 'keys':
            return properties.keys()
        else:
            self.fc = properties[self.name]["f'c"]
            self.e_ult = properties[self.name]['e_ult']

    def getRuptureStrain(self):
        fr = 7.5 * sqrt(-self.fc)
        Ec = 57000 * sqrt(-self.fc)

        er = fr / Ec
        return er

    def getStress(self, strain):
        if self.stress_strain_m == 'hognestad':
            Ec = 57000 * sqrt(-self.fc)

            # rupture info
            fr = 7.5 * sqrt(-self.fc)
            er = fr / Ec

            # Height of stress apex
            fcc = 0.9 * self.fc
            e0 = 1.8 * fcc / Ec

            if er < strain:
                f = 0
            elif 0 <= strain and strain < er:
                f = strain * Ec
            elif e0 < strain < 0:
                f = fcc * (2 * strain / e0 - (strain / e0 )*(strain / e0 ))
            elif self.e_ult <= strain <= e0:
                f = fcc * (1 + 0.15 * (strain - e0)/(e0 - self.e_ult))
            else:
                print(f'Strains under {strain} causes concrete to crush')
                f = 0
            return f
        elif self.stress_strain_m == 'linear':
            Ec = 57000 * sqrt(-self.fc)

            # rupture info
            fr = 7.5 * sqrt(-self.fc)
            er = fr / Ec

            if er < strain:
                f = 0
            elif 0 <= strain and strain < er:
                f = strain * Ec
            elif self.e_ult <= strain < 0:
                f = strain * Ec
            else:
                print(f'Strains under {strain} causes concrete to crush')
                f = 0
            return f



# Run main program
if __name__ == '__main__':
    test = Concrete()


    x = linspace(150e-5, -0.0038, 100)
    y = zeros_like(x)

    for i in range (x.size):
        y[i] = test.getStress(x[i])

    plt.plot(x, y, '-b')
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.show()