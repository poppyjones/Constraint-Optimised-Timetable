from definitions import days_to_hrs, DAYS, TIMESLOTS

def get_timeslots_of_day(all_timeslots, day):
    ar = all_timeslots[days_to_hrs[day]:days_to_hrs[day]+24]
    return ar

def get_timeslots_in_interval(all_timeslots, h0, h1):
    ar = []
    for day in DAYS:
        if h0 < h1:
            ar.extend(all_timeslots[days_to_hrs[day]+h0: days_to_hrs[day]+h1])
        else:
            ar.extend(all_timeslots[days_to_hrs[day]: days_to_hrs[day]+h1])
            ar.extend(all_timeslots[days_to_hrs[day]+h0: days_to_hrs[day]+24])
    return ar

def sum_of_activities_in_timeslots(mdl, timeslots, ACTIVITIES, increment=1):
    counter = []
    for t in timeslots:
        x = mdl.integer_var(domain = [0,increment])
        mdl.add(((t <= ACTIVITIES) & (x == increment))
                | ((t > ACTIVITIES) & (x == 0)))
        counter.append(x)
    return sum(counter)

def sum_of_activities_in_day(mdl, all_timeslots, ACTIVITIES, day, increment=1):
    return sum_of_activities_in_timeslots(mdl, get_timeslots_of_day(all_timeslots, day), ACTIVITIES, increment)

def get_distance(mdl, a0, a1):
    dist = mdl.integer_var(domain = range(TIMESLOTS))
    mdl.add(((a0 <= a1) & (dist == (a1 - a0))) |
            ((a0 > a1) & (dist == TIMESLOTS - (a0 - a1))))
    return dist

def check_distance_within_boundary(mdl, a0, a1, max_distance):
    d = get_distance(mdl, a0, a1)
    accepted = mdl.integer_var(min = 0, max = 1)
    mdl.add(((d <= max_distance) & (accepted == 1))
            | ((d > max_distance) & (accepted == 0)))
    return accepted
