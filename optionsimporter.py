import json


def from_json():
    print("please enter filename:")
    name = input()

    f = open(name, "r")
    d = json.load(f)
    f.close()
    return d