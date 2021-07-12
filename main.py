from ed import ed
from update import update_replit
from package import load_pkg, make_pkg, PackageError, PackageNotFound, FormatError, NameTaken
import random
import shutil
import os
import json
from flask import Flask, request, Response, abort, redirect
import requests
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
  name = request.form.get("name", request.args.get("name"))
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  try:
    return json.dumps(load_pkg(ed.encode(name)))
  except PackageNotFound:
    return f"Package '{name}' was not found", 404
  except Exception as e:
    return f"something went wrong, this is the python error\n{type(e).__name__}: {e}\nrolling back changes", 400

@app.route('/pkg/get/readme', methods=["GET", "POST"])
def editpkg():
  name = get("name")
  version = get("version")
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  elif version == None:
    return f"the arg 'version' is required and was not provided", 400
  full_name = f"{name}_{version}"
  root = os.path.join("pkgs", ed.encode(full_name))
  content = None
  with open(os.path.join(root, "README.md")) as f:
    content = f.read()
  return content

@app.route('/pkg/make', methods=["GET", "POST"])
def makepkg():
  requires_auth(get("token"))
  name = get("name")
  version = get("version")
  username = get("username")
  data = json.loads(get("data"))
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  elif version == None:
    return f"the arg 'version' is required and was not provided", 400
  elif username == None:
    return f"the arg 'username' is required and was not provided", 400
  elif data == None:
    return f"the arg 'data' is required and was not provided", 400
  try:
    make_pkg(username, name, version, data)
  except NameTaken:
    return "name taken", 400
  except FormatError:
    return "format is not met", 400
  except Exception as e:
    shutil.rmtree(os.path.join("pkgs", ed.encode(f"{name}_{version}")))
    os.system("replit push") 
    return f"something went wrong, this is the python error\n{type(e).__name__}: {e}\nrolling back changes", 400
  return "success"

@app.route('/pkg/edit/readme', methods=["GET", "POST"])
def editpkg():
  requires_auth(get("token"))
  name = get("name")
  version = get("version")
  username = get("username")
  newcontent = json.loads(get("newcontent"))
  if name == None:
    return f"the arg 'name' is required and was not provided", 400
  elif version == None:
    return f"the arg 'version' is required and was not provided", 400
  elif username == None:
    return f"the arg 'username' is required and was not provided", 400
  elif newcontent == None:
    return f"the arg 'newcontent' is required and was not provided", 400
  full_name = f"{name}_{version}"
  root = os.path.join("pkgs", ed.encode(full_name))
  with open(os.path.join(root, "README.md"), "w") as f:
    f.write(newcontent)
  return "success"

# docs
@app.route('/<path:path>/docs')
def _docs(path):
  url = f"https://justa6.repl.co/projects/europalang/docs/{path}"
  if url_exists(url):
    return redirect(url)
  else:
    npath = path
    while not url_exists(url):
      npath = "/".join(npath.split("/")[0:-1])
      if npath == "/" or npath == "":
        abort(404)
      url = f"https://justa6.repl.co/projects/europalang/docs/{npath}"
  return redirect(url)
@app.route('/docs')
def docs():
  return redirect("https://justa6.repl.co/projects/europalang/docs")

@app.errorhandler(403)
def forbidden(e):
  return 'you do not have the required auth for this action', 403
app.run(host='0.0.0.0', port=8080)