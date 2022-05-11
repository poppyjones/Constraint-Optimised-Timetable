import json
import os
from definitions import days_to_hrs


class Options:
    def __init__(self):
        # time slot blockers
        self.sleep = [0, 0]
        self.remove_weekend = False
        self.other_blocked = []
        self.preferred_hours = []
        self.preferred_days = []
        self.disliked_hours = []
        self.disliked_days = []
        self.neighborhood = 0
        self.soft_max = 0
        self.hard_max = 0


def from_json():
    print("please enter options filename:")
    name = input()

    with open(name, "r") as f:
        d = json.load(f)

    # Options objects
    opt = Options()

    # Identify all blocked timeslots

    for res_type, value in zip(d["domain restrictions"].keys(), d["domain restrictions"].values()):
        if(res_type == "sleep start"):
            opt.sleep[0] = value
        elif(res_type == "sleep end"):
            opt.sleep[1] = value
        elif(res_type == "remove weekend"):
            opt.remove_weekend = value
        elif(res_type == "otherActivities"):
            oa = value
            for day in oa:
                print(day)
                print(oa[day])
                if len(oa[day]) != 0:
                    opt.other_blocked.extend(
                        map(lambda h: (h[1], days_to_hrs[day]+h[0]), oa[day]))

    # Identify preferences
    for pref_type, value in zip(d["preferences"].keys(), d["preferences"].values()):
        if(pref_type == "preferred hours"):
            for hours in value:
                opt.preferred_hours.append((hours[0], hours[1]))
        elif(pref_type == "disliked hours"):
            for hours in value:
                opt.disliked_hours.append((hours[0], hours[1]))
        elif(pref_type == "preferred days"):
            opt.preferred_days = value
        elif(pref_type == "disliked days"):
            opt.disliked_days = value
        elif(pref_type == "neighborhood"):
            opt.neighborhood = value
        elif(pref_type == "max daily hours"):
            for max_type, value in zip(value.keys(), value.values()):
                if max_type == "hard":
                    opt.hard_max = value
                elif max_type == "soft":
                    opt.soft_max = value

    name = os.path.basename(name)[:-5]
    return name, opt
