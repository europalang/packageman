from ed import ed
from update import update_replit
from package import load_pkg, make_pkg, PackageError, PackageNotFound, FormatError, NameTaken, get_pkg_zip
import random
import os
import json
import io
from flask import Flask, request, Response, abort, redirect, send_file
import requests
import shutil
class MyResponse(Response):
    default_mimetype = 'text/plain'
app = Flask('app')
app.response_class = MyResponse

def requires_auth(token):
	if token != os.environ.get("token"):
		abort(403)

def url_exists(url):
    """Boolean return - check to see if the site exists.
       This function takes a url as input and then it requests the site 
       head - not the full html and then it checks the response to see if 
       it's less than 400. If it is less than 400 it will return TRUE 
       else it will return False.
    """
    try:
            site_ping = requests.head(url)
            if site_ping.status_code < 400:
                return True
            else:
                return False
    except Exception:
        return False

def get(name):
  return request.form.get(name, request.args.get(name))

@app.route('/')
def home():
  return 'This is an api for EuropaPkgMan. It is not finished. Also, for making projects you need to use the interface that doesnt exist right now. Anyways, docs at /docs'

@app.route('/pkg/get', methods=["GET", "POST"])
def getpkg():
  name = get("name")
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  try:
    return json.dumps(load_pkg(ed.encode(name)))
  except PackageNotFound:
    return f"Package '{name}' was not found", 404
  except Exception as e:
    return f"something went wrong, this is the python error\n{type(e).__name__}: {e}\nrolling back changes", 400

@app.route('/pkg/get/zip', methods=["GET", "POST"])
def getpkgzip():
  name = get("name")
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  zippath, mimetype, download_name, as_attachment = get_pkg_zip(name)
  return send_file(zippath,mimetype = mimetype,download_name=download_name,as_attachment = as_attachment)
  

@app.route('/pkg/get/readme', methods=["GET", "POST"])
def getpkgreadme():
  name = get("name")
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  root = os.path.join("pkgs", ed.encode(name))
  content = None
  with open(os.path.join(root, "README.md")) as f:
    content = f.read()
  return content

@app.route('/pkg/make', methods=["GET", "POST"])
def makepkg():
  requires_auth(get("token"))
  name = get("name")
  username = get("username")
  data = json.loads(get("data"))
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  elif username == None:
    return f"the arg 'username' is required and was not provided", 400
  elif data == None:
    return f"the arg 'data' is required and was not provided", 400
  try:
    make_pkg(username, name, data)
  except NameTaken:
    return "name taken", 400
  except FormatError:
    return "format is not met", 400
  except Exception as e:
    try:
      shutil.rmtree(os.path.join("pkgs", ed.encode(name)))
    except Exception:
      pass
    update_replit()
    return f"something went wrong, this is the python error\n{type(e).__name__}: {e}\nrolling back changes", 500
  return "success"

@app.route('/pkg/edit/readme', methods=["GET", "POST"])
def editpkgreadme():
  requires_auth(get("token"))
  name = get("name")
  username = get("username")
  content = get("content")
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  elif username == None:
    return f"the arg 'username' is required and was not provided", 400
  elif content == None:
    return f"the arg 'content' is required and was not provided", 400
  root = os.path.join("pkgs", ed.encode(name))
  info = json.load(open(os.path.join(root, "info.json")))
  if username == info["owner"]:
    with open(os.path.join(root, "README.md"), "w") as f:
      f.write(content)
    return "success"
  else:
    return "user is not the owner of this project", 403

@app.route('/pkg/list', methods=["GET", "POST"])
def getpkglist():
  length = get("length")
  if length == None:
    return f"the arg 'length' is required and was not provided", 400
  elif not length.isdigit():
    return f"the arg 'length' needs to be a vaild number", 400
  length = int(length)
  l = []
  n = 0
  for f in os.scandir('pkgs'):
    if n==length:
      return json.dumps(l)
    if f.is_dir():
      l.append(f.name)
      n+=1
  if n==length:
      return json.dumps(l)
  return 'that is more than the amount of listings', 400
  

# docs
@app.route('/docs')
def docs():
  return redirect("https://europa-docs.europalang.repl.co/Package%20Manager")

@app.errorhandler(403)
def forbidden(e):
  return 'you do not have the required auth for this action', 403
app.run(host='0.0.0.0', port=8080)