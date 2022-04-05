from definitions import DAYS

def print_activities_to_console(msol,fixed, flex):
    print(" Fixed:")
    for s in sorted(fixed,key=lambda s:msol[s]):
        print("  " + s.name + ": "+ str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))
    print(" Flex:")
    for s in sorted(flex,key=lambda s:msol[s]):
        print("  " + s.name + ": "+ str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))
    print()


def print_non_activities_to_console(msol,free):
    print(" Free:")
    for s in sorted(free,key=lambda s:msol[s]):
        print("  " + s.name + ": "+ str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))

def print_timeslots_to_console(msol,hrs,activities):
    n = 0
    for hr in hrs:
        if(n%24==0):
            print(DAYS[int(n/24)])
        print("  " + hr.name + ": "+ activities[msol[hr]].name)
        n = n+1
   
def print_non_empty_timeslots_to_console(msol,hrs,activities,free):
    n = 0
    free_set = set(free)
    for hr in hrs:
        if(n%24==0):
            print(DAYS[int(n/24)])
        if(activities[msol[hr]] not in free_set):
            print("  " + hr.name + ": "+ activities[msol[hr]].name)
        n = n+1
