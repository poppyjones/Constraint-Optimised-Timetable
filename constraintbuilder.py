import helperfunctions as h
import definitions as d

objective = []

#------------------
# Hard Optional
#------------------

def hard_no_weekend(mdl,flex):
    for fl in flex:
        mdl.add( fl != h for h in d.WEEKEND)

def hard_max_daily_hours(model,hrs):
    mdl = model.mdl
    all_timeslots = model.all_timeslots 
    ACTIVITIES = model.ACTIVITIES
    for day in d.DAYS:
        mdl.add(h.sum_of_fixed_flex_in_day(mdl,all_timeslots,ACTIVITIES,day) <= hrs)

#------------------
# Soft Optional
#------------------

def min_max_day(mdl,all_timeslots,ACTIVITIES, day, minimize=True):
    if minimize:
        objective.append(24 - h.sum_of_fixed_flex_in_day(mdl,all_timeslots,ACTIVITIES,day))
    else:
        objective.append(h.sum_of_fixed_flex_in_day(mdl,all_timeslots,ACTIVITIES,day))

def soft_max_daily_hours(model,hr_limit):
    mdl = model.mdl
    all_timeslots = model.all_timeslots 
    ACTIVITIES = model.ACTIVITIES
    penalties = []
    for day in d.DAYS:
        penalty = 5 * ((24-hr_limit) - mdl.max(0,h.sum_of_fixed_flex_in_day(mdl,all_timeslots,ACTIVITIES,day) - hr_limit))
        penalties.append(penalty)
    objective.extend(penalties)

def add_preferred_hours(model, h0, h1):
    timeslots = h.get_timeslots_in_interval(model.all_timeslots,h0,h1)
    objective.append( 5 * h.sum_of_fixed_flex_in_timeslots(model.mdl, timeslots, model.ACTIVITIES))

def add_disliked_hours(model, h0, h1):
    timeslots = h.get_timeslots_in_interval(model.all_timeslots,h0,h1)
    objective.append( 5 * (len(timeslots) - h.sum_of_fixed_flex_in_timeslots(model.mdl, timeslots, model.ACTIVITIES)))

def set_preferred_neighborhood(mdl,a0,activities,max_distance):
    dist_score =  [h.check_distance_within_boundary(mdl,a0, a1, max_distance) for a1 in activities]
    objective.append(5*mdl.max(dist_score))

def set_preferred_neighbor(mdl,a0,a1):
    objective.append(h.check_distance_within_boundary(mdl,a0, a1, 1))

def set_preferred_neighbors(mdl,a0,activities):
    dist_score =  [h.check_distance_within_boundary(mdl,a0, a1, 1) for a1 in activities]
    objective.append(mdl.max(dist_score))

def set_neighbors_of_course_activities(model):
    for c in model.courses:
        # Add preference for each flex activity to be placed exacty before the next flex activity of the same course
        if len(c.flex) >= 2:
            for f0, f1 in zip(c.flex, c.flex[1:]+c.flex[:1]):
                set_preferred_neighbor(model.mdl,f0,f1)
        if len(c.fixed) > 0:
            for f in c.flex:
                # Add preference for being placed exactly before a fixed activity of the same course
                set_preferred_neighbors(model.mdl,f,c.fixed)


def set_neighborhood_of_course_activities(model,max_distance):
    for c in model.courses:
        for f in c.flex:
            if len(c.fixed) > 0:
                # Add preference for being placed in a timeslots close to a fixed activity of the same course
                set_preferred_neighborhood(model.mdl,f,c.fixed,max_distance)

#
# def build(model, imported_options):

def build(model, options):
    #required objective
    set_neighbors_of_course_activities(model)

    #optional objectives
    for h0, h1 in options.preferred_hours:
        add_preferred_hours(model,h0,h1)
    for h0, h1 in options.disliked_hours:
        add_disliked_hours(model,h0,h1)
    for d in options.preferred_days:
        min_max_day(model.mdl,model.all_timeslots,model.ACTIVITIES,d,minimize=False)
    for d in options.disliked_days:
        min_max_day(model.mdl,model.all_timeslots,model.ACTIVITIES,d,minimize=True)
    if options.neighborhood != 0:
        set_neighborhood_of_course_activities(model,options.neighborhood)
    if options.hard_max != 0:
        hard_max_daily_hours(model, options.hard_max)
    if options.soft_max != 0:
        soft_max_daily_hours(model, options.soft_max)


    model.mdl.add(model.mdl.maximize(sum(objective)))
