from load_package import load_pkg
import os
import requests

name = input("Name: ")
files, folders = load_pkg(name)

for folder in folders:
  os.makedirs(os.path.join(name, folder), exist_ok=True)
for filename in files:
  with open(name+filename, "w") as f:
    f.write(files[filename])