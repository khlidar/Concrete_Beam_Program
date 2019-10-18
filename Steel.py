'''
Description:
    Definition of steel class

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

# Definitions
class Steel (object):
    def __init__(self, amount=0, bar_type='#9', location=0, grade='40GR'):
        self.amount = amount  # amount of bars in class
        self.bar_type = bar_type                # bar type according to US naming convention
        self.steel_area = 0                     # Area of steel, based on type and amount
        self.steelArea(amount, bar_type)
        self.location = location                # location of steel in cross section
        self.grade = Grade(grade)               # grade of layer
        self.stress_strain_m = 'trilinear'      # stress-strain method calculated with

    def setSteelInfo(self, bar_type='', amount=0, location='', stress_strain_m=''):
        '''
        Function used to edit steel information

        :param bar_type:
        :param amount:
        :param location:
        :param grade:
        :param stress_strain_m:
        :return:
        '''

        if amount:
            self.amount = amount
            self.steelArea(self.amount, self.bar_type)
        if bar_type:
            self.bar_type = bar_type
            self.steelArea(self.amount, self.bar_type)
        if location:
            self.location = location
        if stress_strain_m:
            if stress_strain_m == 'trilinear':
                self.stress_strain_m = stress_strain_m
            else:
                print(f'"{stress_strain_m}" is not valid stress_strain_method in class Steel')
                print('Valid inputs are: "trilinear"')

    def getLocation(self):
        return self.location

    def getAmount(self):
        return self.amount

    def getBarType(self):
        return self.bar_type

    def getStealArea(self):
        return self.steel_area

    # Changes the grade of the steel
    def changeGrade(self, new_grade):
        self.grade.changeGrade(new_grade)

    #plots Stress-strain curve of steel
    def Plot_S_S_curve(self):
        if self.stress_strain_m == 'trilinear':
            strain_y = self.grade.stress_y()/self.grade.E
            x = [0, strain_y, self.grade.strain_sh(), self.grade.strain_u()]
            y = [0, self.grade.stress_y(), self.grade.stress_y(), self.grade.stress_u()]

            plt.plot(x, y, '-b')
            plt.grid(True)
            plt.xlabel('Strain')
            plt.ylabel('Stress')
            theTitle = f'Stress-strain curve for steel {self.grade}'
            plt.title(theTitle)
            plt.show()

    def setSSMethod(self, SSMethod):
        '''
        -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
        To do before adding new methods to list
            Add method to stress()
            Add method to Plot_S_S_Curve
        -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
        :param SSMethod:    - String with name of method to be used for stress-strain calculations
        :return:
        '''
        methods = ('trilinear',)
        if SSMethod in methods:
            self.stress_strain_m = SSMethod
        else:
            print(f'"{SSMethod}" is not valid input into Steel.setSSMethod')


    def stress(self, strain):
        '''
        Gives stress in steel due to strain.

        Remember to add name of new method to list of valid methods in SSMethod() after defining new
        stress-strain relationship.
        :param strain:
        :return:
        '''
        if self.stress_strain_m == 'trilinear':
            # here we will do some calculations

            if strain < self.grade.strain_y():           # If steel hasn't yielded, stress = strain * E
                return strain * self.grade.E
            elif strain < self.grade.strain_sh():        # If steel has yielded but hardening not started, stress = fy
                return self.grade.stress_y()
            else:                                   # Steel has yielded and hardening has started
                f = self.grade.stress_y() + self.grade.Esh() * (strain - self.grade.strain_sh())
                if f <= self.grade.stress_u():
                    return f
                else:
                    print(f'Strain {strain} causes steel to break')
                    return 0


        else:
            return 'Just don\'t know at the moment'

    def force(self, strain):
        stress = self.stress(strain)
        return stress*self.steel_area


    def steelArea(self, amount, bar_type):
        # Dictionary of available rebar sizes
        steelarea = {'#3': 0.11,
                     '#4': 0.20,
                     '#5': 0.31,
                     '#6': 0.44,
                     '#7': 0.60,
                     '#8': 0.79,
                     '#9': 1.00,
                     '#10': 1.27,
                     '#11': 1.56,
                     '#14': 2.25,
                     '#18': 4.00}

        # Calculate steel_area if inputs are valid
        if bar_type in steelarea.keys() and amount >= 0:
            self.steel_area = steelarea.get(bar_type) * amount
        else:
            print('invalid input into Steel.steelArea')


class Grade(object):
    '''
    Class that holds the information needed for any given grade
    '''
    def __init__(self, grade='40GR'):
        self.name = grade
        self.gradeInfo(self.name, 'update')

    def gradeInfo(self, name, info):
        properties = {'40GR': {'fy': 40e3, 'fu': 60e3, 'E': 29e6, 'E_sh': 2000e3, 'e_sh': 5.e-3},
                      '60GR': {'fy': 60e3, 'fu': 90e3, 'E': 29e6, 'E_sh': 3000e3, 'e_sh': 3.e-3}}

        if self.name in properties.keys() and info == 'update':
            self.fy = properties[self.name]['fy']
            self.fu = properties[self.name]['fu']
            self.E = properties[self.name]['E']
            self.E_sh = properties[self.name]['E_sh']
            self.e_sh = properties[self.name]['e_sh']

        if info == 'keys':
            return properties.keys()


    def stress_y(self):
        return self.fy

    def stress_u(self):
        return self.fu

    def strain_y(self):
        return self.fy / self.E

    def strain_sh(self):
        return self.e_sh

    def strain_u(self):
        return ((self.fu - self.fy) / self.E_sh) + self.e_sh

    def Esh(self):
        return self.E_sh

    def Emodulus(self):
        return self.E

    def changeGrade(self, new_grade):
        grades = self.gradeInfo(self.name, 'keys')
        if new_grade in grades:
            self.name = new_grade
        else:
            print(f'"{new_grade}" is not valid input into Class Grade.changeGrade')

    def __str__(self):
        return self.name


# Run main program
if __name__ == '__main__':
    steel1 = Steel(5, '#9', 26)
    print(steel1.steel_area)

    test = Grade()

    steel1.Plot_S_S_curve()

'''
    steel1 = Steel()
    print(steel1.stress(0.0062))

    steel1.setSteelInfo(bar_type="#3", amount=5)

    print(steel1.force(0.0062))

    print(steel1.steel_area)

    steel1.Plot_S_S_curve()

    #steel1.Plot_S_S_curve()

'''
