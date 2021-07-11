from flask import Flask
app = Flask('app')

@app.route('/')
def home():
  return 'This is an api for '

app.run(host='0.0.0.0', port=8080)