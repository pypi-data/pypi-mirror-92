class Option:
  def __init__(self, key, value):
    self.key = key
    self.value = value

  def __str__(self):
    return self.key

  def __repr__(self):
    return self.key

