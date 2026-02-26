#Generators are functions that can pause and resume their execution.

# 1 task
def squares_up_to(N):
    for i in range(1, N + 1):
        yield i * i #when yield encountered, function`s state saved, and value returns

N = 5
for val in squares_up_to(N): #executes only when we iterate over generator
    print(val)


# 2 task
def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter n: "))
print(", ".join(str(x) for x in even_numbers(n))) # generator expression


# 3 task
def divisible_by_3_and_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input("Enter n: "))
for val in divisible_by_3_and_4(n):
    print(val)


# 4 task
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

for val in squares(1, 5):
    print(val)


# 5 task
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

for val in countdown(5):
    print(val)