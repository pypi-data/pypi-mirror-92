import os

def resolve(value):
  print(os.environ.keys())

  if value[0:1] == "$":
    name = value[1:]
    value = os.environ.get(name, value)
    print(f"Resolved {name} to {value}")

  return value
