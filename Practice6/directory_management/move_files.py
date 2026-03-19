import shutil
import os

os.makedirs("folder_1", exist_ok=True)
os.makedirs("folder_2", exist_ok=True)

with open("example.txt", "w") as file:
    file.write("Test file")

shutil.move("example.txt", "folder_1/example.txt")
print("File moved")

shutil.copy("folder_1/example.txt", "folder_2/example_copy.txt")
print("The file has been copied back")