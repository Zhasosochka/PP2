class Animal:
    def speak(self):
        print("The animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("Woof! Woof!")

my_pet = Dog()
my_pet.speak()