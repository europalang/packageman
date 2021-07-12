import re

class encodedecode():
  def __init__(self, badchars):
    badchars = list(badchars)
    badchars.append("[")
    badchars.append("]")
    self.badchars = badchars
  def encode(self, text):
    text = list(text)
    newtext = ""
    for char in text:
      if char in self.badchars:
        newtext+=f"[{ord(char)}]"
      else:
        newtext+=char
    return newtext
  def decode(self, text):
    newtext = text
    matches = re.findall(r"\[.*?\]", newtext)
    for match in matches:
      n = match[1:-1]
      print(n)
      if n.isdigit():
        n = int(n)
        newtext = newtext.replace(match, chr(n), 1)
    return newtext

ed = encodedecode("/.\\") # This is just for this project, do not need to include if copying