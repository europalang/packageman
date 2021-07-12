from threading import Thread
def update_replit():
  def run():
    import os
    os.system("replit push")
  t = Thread(target=run)
  t.start()