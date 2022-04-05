from definitions import days_to_hrs, DAYS

def get_timeslots_of_day(all_timeslots,day):
    ar = all_timeslots[days_to_hrs[day]:days_to_hrs[day]+24]
    return ar

def get_timeslots_in_interval(all_timeslots, h0, h1):
    ar = []
    for day in DAYS:
        ar.extend(all_timeslots[days_to_hrs[day]+h0:days_to_hrs[day]+h1])
    for a in ar:
        print(a.name)
    return ar

def sum_of_activities_in_timeslots(mdl, timeslots, ACTIVITIES, increment=1):
    counter = []
    for t in timeslots:
        x = mdl.binary_var()
        mdl.add( ((t <= ACTIVITIES) & (x == increment )) | ((t > ACTIVITIES) & (x == 0)) )
        counter.append(x)
    return sum(counter)

def sum_of_activities_in_day(mdl,all_timeslots, ACTIVITIES, day, increment=1):
    return sum_of_activities_in_timeslots(mdl,get_timeslots_of_day(all_timeslots,day), ACTIVITIES, increment)