from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map applies funtion to all elements
squared = list(map(lambda x: x**2, numbers))
print("Squires:", squared)


even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

sum_all = reduce(lambda x, y: x + y, numbers)
print("Sum:", sum_all)