import os
from ed import ed

class PackageError(Exception): pass
class PackageNotFound(PackageError): pass
class FormatError(PackageError): pass
class NameTaken(PackageError): pass

def load_pkg(name):
  folder = os.path.join("pkgs", name)
  if not os.path.exists(folder):
    raise PackageNotFound("Package not found")
  filenames = []
  files = {}
  folders = []
  i = {}
  _folder = folder
  for root, dirs, _files in os.walk(folder):
    for file in _files:
      f = os.path.join(root,file)
      if not f.replace(_folder, "", 1).startswith("/info"):
        filenames.append(f)
      else:
        with open(f) as fi:
          i[file] = fi.read()
    for folder in dirs:
      f = os.path.join(root.replace(_folder, "", 1),folder)
      if not f=="info":
        folders.append(f)
  for filename in filenames:
   with open(filename) as f:
     files[filename.replace(_folder, "", 1)] = f.read()
  i.update({"files":files,"folders":folders})
  return i

def is_bad(data):
  files = data["files"]
  folders = data["folders"]
  required_folders = ["files"]
  optional_folders = ["docs"]
  free_to_edit = ["files", "docs"]
  for rfolder in required_folders:
    if not rfolder in folders:
      return True
  for folder in folders:
    if folder not in optional_folders:
      fparts = folder.split("/")
      if fparts[0] == '':
        del fparts[0]
      if not fparts[0] in free_to_edit:
        return True
#  for file in files:
#    fparts = folder.split("/")
#    if fparts[0] == '':
#      del fparts[0]
#    if not fparts[0] in free_to_edit:
#      return True
  return False
def make_pkg(username, name, data):
  root = os.path.join("pkgs", ed.encode(name))
  if os.path.exists(root):
    raise NameTaken
  if is_bad(data):
    raise FormatError
  os.makedirs(root)
  files = data["files"]
  folders = data["folders"]
  for folder in folders:
    os.makedirs(os.path.join(root, folder), exist_ok=True)
  for filename in files:
    with open(root+filename, "w") as f:
      f.write(files[filename])
  info = os.path.join(root, 'info')
  os.makedirs(info,exist_ok=True)
  with open(os.path.join(info, "owner"), "w") as f:
    f.write(username)