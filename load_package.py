import os

class PackageError(Exception): pass
class PackageNotFound(PackageError): pass

def load_pkg(name):
  folder = os.path.join("pkgs", name)
  if not os.path.exists(folder):
    raise PackageNotFound("Package not found")
  filenames = []
  files = {}
  folders = []
  _folder = folder
  for root, dirs, _files in os.walk(folder):
    for file in _files:
      filenames.append(os.path.join(root,file))
    for folder in dirs:
      folders.append(os.path.join(root.replace(_folder, "", 1),folder))
  for filename in filenames:
   with open(filename) as f:
     files[filename.replace(_folder, "", 1)] = f.read()
  return files, folders
