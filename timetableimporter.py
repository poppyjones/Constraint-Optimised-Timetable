import json
from definitions import days_to_hrs


def from_json():
    print("please enter filename:")
    name = input()

    f = open(name, "r")
    d = json.load(f)
    f.close()

    fixed_activities = []
    all_activities  = []

    fa = d["fixedActivities"]
    # loop through days
    for day in fa.keys():
        print(day)
        print(fa[day])
        if len(fa[day].keys()) != 0:
            # add names of planned activities
            all_activities.extend(fa[day].values())
            # add times of planned activities
            fixed_activities.extend(map(lambda h: days_to_hrs[day]+int(h),fa[day].keys()))

    all_activities.extend(d["flexActivities"])
    
    return (all_activities,fixed_activities)
    
def from_file():
    raise NotImplementedError()
    print("please enter filename:")
    name = input()
    f = open(name, "r")



def from_excel():
    raise NotImplementedError()