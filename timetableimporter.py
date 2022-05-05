import json
import os
from definitions import days_to_hrs


def from_json():
    print("please enter filename for data file:")
    file_name = input()

    with open(file_name, "r") as f:
        d = json.load(f)

    courses = []
    a = 0

    for name, course in zip(d["courses"].keys(), d["courses"].values()):
        fixed_activities = []
        flex_activities  = []
        # get name of course
        print("importing: " + name)
        
        # loop through days to add fixed activities
        fa = course["fixedActivities"]
        for day in fa.keys():
            print(day)
            print(fa[day])
            if len(fa[day]) != 0:
                fixed_activities.extend(map(lambda h: (name + ": " + h[1], days_to_hrs[day]+h[0]),fa[day]))
        # Add a name for each flex activity
        flex_activities = [name + ": Flex " + str(x) for x in range(1,course["flexActivities"]+1)] 

        # Add number of course activities to total number of activities
        a += len(flex_activities) + len(fixed_activities)

        courses.append((name, fixed_activities, flex_activities))
    print("import complete:")
    file_name = os.path.basename(file_name)[:-5]
    print(f"  Filename: {file_name}")
    print(f"  Number of courses: {str(len(courses))}")
    print(f"  Number of activities: {str(a)}")
    return file_name, courses, a
    
def from_file():
    raise NotImplementedError()
    print("please enter filename:")
    name = input()
    f = open(name, "r")



def from_excel():
    raise NotImplementedError()