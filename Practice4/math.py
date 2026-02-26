import math

#1 task
degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)
print(f"Output radian: {radian:6f}")

#2 task
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area = ((base1 + base2) / 2) * height
print(f"Expected Output: {area:.1f}")

#3 task s = a^2 * n / 4tg(pi/n)
n = int(input("Input number of sides: "))
length = float(input("Input the length of a side: "))
polygon_area = (n * pow(length, 2)) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {polygon_area:.0f}")

#4 task
base = float(input("Length of base: "))
p_height = float(input("Height of parallelogram: "))
parallelogram_area = base * p_height
print(f"Expected Output: {parallelogram_area}")