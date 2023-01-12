print("Content-type application/json")
print("")

import json
obj = None
with open("example.json", "r") as file:
    obj = json.load(file)
print(json.dumps(obj))