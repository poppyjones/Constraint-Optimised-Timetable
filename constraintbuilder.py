import helperfunctions as h
import definitions as d

score = []

#------------------
# Hard Optional
#------------------

def hard_no_weekend(mdl,flex):
    for fl in flex:
        mdl.add( fl != h for h in d.WEEKEND)

def hard_max_daily_hours(mdl,all_timeslots,ACTIVITIES,hrs):
    for day in d.DAYS:
        mdl.add(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,day) <= hrs)

#------------------
# Soft Optional
#------------------

def soft_min_max_day(mdl,all_timeslots,ACTIVITIES, day, minimize=True):
    score.append(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,day, -1 if minimize else 1))

def soft_min_max_weekend(mdl,all_timeslots,ACTIVITIES,minimize=True):
    soft_min_max_day(mdl,all_timeslots,ACTIVITIES, d.SAT, minimize)
    soft_min_max_day(mdl,all_timeslots,ACTIVITIES, d.SUN, minimize)

def soft_max_daily_hours(mdl,all_timeslots,ACTIVITIES,hr_limit):
    penalties = []
    for day in d.DAYS:
        penalties.append(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,day) - hr_limit)
    score.extend(penalties)

def add_preffered_hours(mdl,all_timeslots,ACTIVITIES, h0, h1):
    timeslots = []
    if h0 <= h1:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,h1)
    else:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,24)
        timeslots.extend(h.get_timeslots_in_interval(all_timeslots,0,h1))
    score.append(h.sum_of_activities_in_timeslots(mdl, timeslots, ACTIVITIES,5))

def add_disliked_hours(mdl,all_timeslots,ACTIVITIES, h0, h1):
    timeslots = []
    if h0 <= h1:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,h1)
    else:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,24)
        timeslots.extend(h.get_timeslots_in_interval(all_timeslots,0,h1))
    score.append(h.sum_of_activities_in_timeslots(mdl, timeslots, ACTIVITIES,-5))

def set_preffered_neighborhood(mdl,a0,activities,max_distance):
    dist_score =  [h.check_distance_within_boundary(mdl,a0, a1, max_distance) for a1 in activities]
    score.append(2*mdl.max(dist_score))

def set_preffered_neighbor(mdl,a0,a1):
    score.append(h.check_distance_within_boundary(mdl,a0, a1, 1))

def set_preffered_neighbors(mdl,a0,activities):
    dist_score =  [h.check_distance_within_boundary(mdl,a0, a1, 1) for a1 in activities]
    score.append(mdl.max(dist_score))

def set_neighborhood_of_course_activities(mdl,courses,max_distance):
    for c in courses:
        if len(c.flex) >= 2:
            for f0, f1 in zip(c.flex, c.flex[1:]+c.flex[:1]):
                set_preffered_neighbor(mdl,f0,f1)
        if len(c.fixed) == 0:
            continue
        for f in c.flex:
            set_preffered_neighborhood(mdl,f,c.fixed,max_distance)
            set_preffered_neighbors(mdl,f,c.fixed)


def build(mdl, all_timeslots, ACTIVITIES, flex, courses):
    
    # TODO: IMPORT FROM OPTIONSIMPORTER
    hard_no_weekend(mdl,flex)
    hard_max_daily_hours(mdl,all_timeslots,ACTIVITIES,8)
    soft_max_daily_hours(mdl,all_timeslots,ACTIVITIES,7)
    #soft_min_max_day(mdl,all_timeslots,ACTIVITIES, d.FRI, minimize=True)
    set_neighborhood_of_course_activities(mdl,courses,24)
    set_neighborhood_of_course_activities(mdl,courses,5)

    
    add_preffered_hours(mdl,all_timeslots,ACTIVITIES,8,12)
    add_preffered_hours(mdl,all_timeslots,ACTIVITIES,10,16)

    add_disliked_hours(mdl,all_timeslots,ACTIVITIES,12,13)
    add_disliked_hours(mdl,all_timeslots,ACTIVITIES,12,13)

    add_preffered_hours(mdl,all_timeslots,ACTIVITIES,20,22)


    mdl.add(mdl.maximize(sum(score)))
