from ed import ed
from package import load_pkg, make_pkg, PackageError, PackageNotFound, FormatError, NameTaken
import shutil
import os
import json
from flask import Flask, request, Response, abort
class MyResponse(Response):
    default_mimetype = 'text/plain'
app = Flask('app')
app.response_class = MyResponse

def requires_auth(token):
	print(token, os.environ['token'])
	if token != os.environ.get("token"):
		abort(403)

def get(name):
  return request.form.get(name, request.args.get(name))

@app.route('/')
def home():
  return 'This is an api for EuropaPkgMan. It is not finished, and there is no docs'

@app.route('/pkg/get', methods=["GET", "POST"])
def getpkg():
  name = request.form.get("name", request.args.get("name"))
  try:
    return json.dumps(load_pkg(ed.encode(name)))
  except PackageNotFound:
    return f"Package '{name}' was not found", 404

@app.route('/pkg/make', methods=["GET", "POST"])
def makepkg():
  requires_auth(get("token"))
  name = request.form.get("name", request.args.get("name"))
  username = request.form.get("username", request.args.get("username"))
  data = json.loads(request.form.get("data", request.args.get("data")))
  try:
    make_pkg(username, name, data)
  except NameTaken:
    return "name taken", 400
  except FormatError:
    return "format is not met", 400
  except Exception as e:
    shutil.rmtree(os.path.join("pkgs", ed.encode(name)))
    return f"something went wrong, this is the python error\n{type(e).__name__}: {e}\nrolling back changes", 400
  return "success"

@app.errorhandler(403)
def forbidden(e):
  return 'you do not have the required auth for this action', 403
app.run(host='0.0.0.0', port=8080)