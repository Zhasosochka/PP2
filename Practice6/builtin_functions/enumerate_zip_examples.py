names = ["Adilkhan", "Al-Mukhammad", "Zhaslan", "Tair", "Alim"]
scores = [85, 90, 78, 69, 67]

print("Index list:")
for index, name in enumerate(names):
    print(index, name)

print("\nZipped data:")
for name, score in zip(names, scores):
    print(name, score)