from threading import Thread
def update_replit():
  def run():
    try:
      import os
      os.system("replit push")
    except:
      pass
  t = Thread(target=run)
  t.start()