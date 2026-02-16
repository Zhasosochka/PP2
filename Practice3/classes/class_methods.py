class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, I am " + self.name)

p1 = Person("Rauan")
p1.greet()