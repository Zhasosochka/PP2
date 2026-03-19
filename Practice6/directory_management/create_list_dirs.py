import os

os.makedirs("test_dir/sub_dir", exist_ok=True)
print("Folder created\n")

print("Content of current folder:")
items = os.listdir("test_dir")

for item in items:
    print(item)