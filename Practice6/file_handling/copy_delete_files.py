import shutil
import os

print("Choose action:\n-Copy (to create copy of sample file)\n-Delete (to delete sample copy)")
action = input()

if action == "Copy":
    shutil.copy("sample.txt", "sample_copy.txt")
    print("File was copied!")

elif action == "Delete":
    if os.path.exists("sample_copy.txt"):
        os.remove("sample_copy.txt")
        print("Copy was deleted!")
    else:
        print("Nothing to Delete")