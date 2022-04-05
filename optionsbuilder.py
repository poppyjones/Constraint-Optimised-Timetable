import helperfunctions as h
import definitions as d

score = []

#------------------
# Hard Optional
#------------------

def hard_no_weekend(mdl,flex):
    for fl in flex:
        mdl.add( fl != n for n in d.WEEKEND)

#------------------
# Soft Optional
#------------------

def soft_min_max_weekend(mdl,all_timeslots,ACTIVITIES,minimize=True):
    p = []
    p.append(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,d.SAT, -1 if minimize else 1))
    p.append(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,d.SUN, -1 if minimize else 1))
    score.extend(p)


def soft_min_max_day(mdl,all_timeslots,ACTIVITIES, day, minimize=True):
    score.append(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,day, -1 if minimize else 1))

def hard_max_daily_hours(mdl,all_timeslots,ACTIVITIES,hrs):
    for day in d.DAYS:
        mdl.add(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,day) <= hrs)

def soft_max_daily_hours(mdl,all_timeslots,ACTIVITIES,hrs):
    penalties = []
    for day in d.DAYS:
        penalties.append(h.sum_of_activities_in_day(mdl,all_timeslots,ACTIVITIES,day) - hrs)
    score.extend(penalties)

def add_preffered_hours(mdl,all_timeslots,ACTIVITIES, h0, h1):
    timeslots = []
    if h0 <= h1:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,h1)
    else:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,24)
        timeslots.extend(h.get_timeslots_in_interval(all_timeslots,0,h1))
    score.append(h.sum_of_activities_in_timeslots(mdl, timeslots, ACTIVITIES))


def add_disliked_hours(mdl,all_timeslots,ACTIVITIES, h0, h1):
    timeslots = []
    if h0 <= h1:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,h1)
    else:
        timeslots = h.get_timeslots_in_interval(all_timeslots,h0,24)
        timeslots.extend(h.get_timeslots_in_interval(all_timeslots,0,h1))
    score.append(h.sum_of_activities_in_timeslots(mdl, timeslots, ACTIVITIES,-1))

#def min_max_active_days(mdl, all_timeslots, ACTIVITIES, activity_req, minimize):
#    increment = -1 if minimize else 1
#    for day in d.DAYS:
#        
#    score.append()

def build(mdl, all_timeslots, ACTIVITIES, flex):
    # TODO: IMPORT FROM OPTIONSIMPORTER
    hard_no_weekend(mdl,flex)
    soft_max_daily_hours(mdl,all_timeslots,ACTIVITIES,7)
    #soft_min_max_day(mdl,all_timeslots,ACTIVITIES, d.TUE, minimize=False)
    
    #add_preffered_hours(mdl,all_timeslots,ACTIVITIES,10,12)
    #add_preffered_hours(mdl,all_timeslots,ACTIVITIES,13,16)
    #add_preffered_hours(mdl,all_timeslots,ACTIVITIES,10,15)
    #add_disliked_hours(mdl,all_timeslots,ACTIVITIES,12,13)
    #add_disliked_hours(mdl,all_timeslots,ACTIVITIES,12,13)

    mdl.add(mdl.maximize(sum(score)))
