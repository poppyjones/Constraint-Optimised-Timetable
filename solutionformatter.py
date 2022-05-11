from definitions import DAYS
from gui import build_output_gui

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

def print_activities_by_course(msol,courses):
    for c in courses:
        print(c.name)
        sorted_activities = sorted((c.flex + c.fixed), key = lambda e: msol[e])
        for s in sorted_activities:
            print("  " + s.name + ": "+ str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))

def append_solution(name,msol):
    
    with open("output/solutions.csv", "a") as f:
        f.write(f"{name}, {msol.get_objective_values()[0]}, {msol.get_objective_bounds()[0]}, {msol.get_objective_gaps()[0]}, {msol.get_solve_time()}\n")

def create_html_timetable(msol,name,courses,other, blocked = []):
    w, h = 7, 24
    timetable = [[0 for _ in range(w)] for _ in range(h)]
    for c in courses:
        for f in c.fixed:
            hr = msol[f]
            timetable[hr%24][hr//24] = (f"fixed {c.name}",f.name)
        for f in c.flex:
            hr = msol[f]
            timetable[hr%24][hr//24] = (f"flex {c.name}",f.name)
    for o in other:
        hr = msol[o]
        timetable[hr%24][hr//24] = (f"other {o.name}",o.name)
    for b in blocked:
        print(f"adding blocked {b.name}")
        hr = msol[b]
        timetable[hr%24][hr//24] = (f"blocked {b.name}",b.name)
    build_output_gui(name,timetable)