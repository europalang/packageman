class encodedecode():
  def __init__(self, badchars):
    badchars = list(badchars)
    self.badchars = badchars.append("[")
    self.badchars = badchars.append("]")
  def encode(self, text):
    text = list(text)
    newtext = ""
    for char in text:
      if char in self.badchars:
        newtext+=f"[{ord(char)}]"
      else:
        newtext+=char
    return newtext