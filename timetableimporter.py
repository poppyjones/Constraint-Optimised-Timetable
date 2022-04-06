import json
from definitions import days_to_hrs


def from_json():
    print("please enter filename:")
    name = input()

    f = open(name, "r")
    d = json.load(f)
    f.close()

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
    print("  Number of courses: " + str(len(courses)))
    print("  Number of activities: " + str(a))
    return courses, a
    #return (all_activities,fixed_activities)
    
def from_file():
    raise NotImplementedError()
    print("please enter filename:")
    name = input()
    f = open(name, "r")



def from_excel():
    raise NotImplementedError()