import json


def from_json():
    print("please enter filename:")
    name = input()

    with open(name, "r") as f:
        f = open(name, "r")
        d = json.load(f)
    
    return d