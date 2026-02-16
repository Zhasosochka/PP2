class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

class Athlete:
    def display_sport(self):
        print("I play Football.")

class StudentAthlete(Person, Athlete):
    pass

x = StudentAthlete("Dastan", "Satpayev")
print(x.firstname)
x.display_sport()