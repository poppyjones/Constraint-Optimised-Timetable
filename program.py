from docplex.cp.model import CpoModel
import solutionformatter
import timetableimporter
from definitions import WEEKEND, TIMESLOTS, DAYS

#-----------------------------------------------------------------------------
# Initialize the problem data
#-----------------------------------------------------------------------------

activity_names, fixed_times = timetableimporter.from_json()

# Empty activity data structures
all_activities = []
fixed = []
flex  = []
free = []

# Empty timeslot data structures
all_timeslots = []*TIMESLOTS

#-----------------------------------------------------------------------------
# Build the model
#-----------------------------------------------------------------------------

# Create model
mdl = CpoModel()

# Add variable for each activity
for i in range(len(activity_names)):
    a = mdl.integer_var(name= activity_names[i], domain= range(0, TIMESLOTS))
    all_activities.append(a)
    if i < len(fixed_times):
        fixed.append(a)
    else:
        flex.append(a)

# Add variables for each free activity
# - assumes at least one empty slot
# - keep them sorted to minimise nr. of solutions
prev_a = mdl.integer_var(name= ("free activity: 0"), domain= range(0, TIMESLOTS))
all_activities.append(prev_a)
free.append(prev_a)

for i in range(1,TIMESLOTS - len(all_activities)):
    a = mdl.integer_var(name= ("free activity: "+str(i)), domain= range(0, TIMESLOTS))
    all_activities.append(a)
    free.append(a)
    mdl.add(prev_a < a)
    prev_a = a


# add variable for each time slot
for i in range(TIMESLOTS):
    mdl.integer_var(name=(DAYS[i//24] + " kl. " + str(i%24)), domain=range(0,len(all_activities)))

#-----------------------------------------------------------------------------
# Add constraints
#-----------------------------------------------------------------------------

#------------------
# Hard Mandatory
#------------------

# set timeslots for fixed activities
for i in range(len(fixed)):
    mdl.add( fixed[i] == fixed_times[i])

# no activities with the same timeslots
mdl.add(mdl.all_diff(all_activities))

#------------------
# Hard Optional
#------------------

# Hard no weekend

for fl in flex:
    mdl.add( fl != n for n in WEEKEND)

#------------------
# Soft Optional
#------------------

# min/max weekend
    # give penalties when weekend timeslots are assigned

#-----------------------------------------------------------------------------
# Solve Model
#-----------------------------------------------------------------------------

msol = mdl.solve(TimeLimit=10)

#-----------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------


#solutionformatter.print_timeslots_to_console(msol,all_timeslots)

solutionformatter.print_activities_to_console(msol,fixed,flex)
