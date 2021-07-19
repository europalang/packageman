import os
from ed import ed
from update import update_replit
import json
import shutil

class PackageError(Exception): pass
class PackageNotFound(PackageError): pass
class FormatError(PackageError): pass
class NameTaken(PackageError): pass
from zipfile import ZipFile

def get_pkg_zip(name, forflask=True):
  zippath = os.path.join("pkg-zips", ed.encode(name))+'.zip'
  pkgfolder = f"pkgs/{ed.encode(name)}/"
  if os.path.isfile(zippath):
    with ZipFile(zippath, 'r') as zf:
      readme = os.path.join(pkgfolder, 'README.md')
      if zf.read('README.md').decode('utf-8') != open(readme).read():
        print('zip is being updated because readme changed')
        os.remove(zippath)
  if not os.path.isfile(zippath):
    print('zip is being created')
    pkgfolder = os.path.join("pkgs", ed.encode(name))
    with ZipFile(zippath, 'w') as zf:
      update_replit()
      for root, dirs, files in os.walk(pkgfolder):
          for file in files:
            filepath = os.path.join(root, file)
            relpath = filepath.replace(pkgfolder, "", 1)
            if not relpath == 'info.json':
               zf.write(filepath, relpath)
               update_replit()
    
    #shutil.make_archive(zippath, 'zip', )
    update_replit()
    #delete_file_from_zip(zippath+".zip", 'info.json')
    #update_replit()
  if forflask:
    return zippath,'zip',name+'.zip',True
  else:
    return zippath+".zip"
def load_pkg(name):
  folder = os.path.join("pkgs", name)
  if not os.path.exists(folder):
    raise PackageNotFound("Package not found")
  filenames = []
  files = {}
  folders = []
  i = {}
  _folder = folder
  content = json.load(open(os.path.join(folder, "info.json")))
  i.update(content)
  for root, dirs, _files in os.walk(folder):
    for file in _files:
      f = os.path.join(root,file)
      with open(f) as fi:
        files[file] = fi.read()
    for folder in dirs:
      f = os.path.join(root.replace(_folder, "", 1),folder)
      folders.append(f)
  for filename in filenames:
   with open(filename) as f:
     files[filename.replace(_folder, "", 1)] = f.read()
  i.update({"files":files,"folders":folders})
  del i["files"]["info.json"]
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
  update_replit()
  files = data["files"]
  folders = data["folders"]
  for folder in folders:
    os.makedirs(os.path.join(root, folder), exist_ok=True)
    update_replit()
  for filename in files:
    with open(root+filename, "w") as f:
      f.write(files[filename])
    update_replit()
  json.dump({"owner": username}, open(os.path.join(root, "info.json"), "w"))
  update_replit()

  # Making zip
  get_pkg_zip(name, forflask=False)

