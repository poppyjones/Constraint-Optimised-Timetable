from definitions import DAYS

def print_activities_to_console(msol,fixed, flex):
    if msol:
        print("Solution:")
        print(" Fixed:")
        for s in sorted(fixed,key=lambda s:msol[s]):
            print("  " + s.name + ": "+ str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))
        print(" Flex:")
        for s in sorted(flex,key=lambda s:msol[s]):
            print("  " + s.name + ": "+ str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))
        print()
    else:
        print("Solve status: " + msol.get_solve_status())

def print_non_activities_to_console(msol,free):
    if msol:
        print(" Free:")
        for s in sorted(free,key=lambda s:msol[s]):
            print("  " + s.name + ": "+ str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))
    else:
        print("Solve status: " + msol.get_solve_status())


def print_timeslots_to_console(msol,hrs,activities):
    n = 0
    for hr in hrs:
        if(n%24==0):
            print(DAYS[int(n/24)])
        print("  " + hr.name + ": "+ activities[msol[hr]].name)
        n = n+1
   
