from docplex.cp.model import CpoModel
from definitions import days_to_hrs

def get_timeslots_of_day(all_timeslots,day):
    ar = all_timeslots[days_to_hrs[day]:days_to_hrs[day]+24]
    return ar

def sum_of_activities_in_timeslots(mdl, timeslots, ACTIVITIES):
    counter = []
    for t in timeslots:
        x = mdl.binary_var()
        mdl.add( ((t <= ACTIVITIES) & (x == 1 )) | ((t > ACTIVITIES) & (x == 0)) )
        counter.append(x)
    return sum(counter)

def sum_of_activities_in_day(mdl,all_timeslots, ACTIVITIES, day):
    return sum_of_activities_in_timeslots(mdl,get_timeslots_of_day(all_timeslots,day), ACTIVITIES)