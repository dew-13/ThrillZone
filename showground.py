#
# Student Name : Ima Student
# Student ID   : 12345678
#
# showground.py - classes for simulation of rides in a showground
#

class Pirate():
    """Class to represent Pirate rides in showground"""

    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def plot_me(self, p):
        p.plot([0, self.xpos], [0,self.ypos])

    def step_change(self):
        self.xpos = self.xpos + 10




