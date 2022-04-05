from docplex.cp.model import CpoModel
import solutionformatter
import timetableimporter
import optionsbuilder
import helperfunctions
from definitions import WEEKEND, TIMESLOTS, DAYS, MON, FRI

#-----------------------------------------------------------------------------
# Initialize the problem data
#-----------------------------------------------------------------------------

activity_names, fixed_times = timetableimporter.from_json()

ACTIVITIES = len(activity_names)

# Empty activity data structures
all_activities = []*ACTIVITIES
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

for i in range(1,1 + TIMESLOTS - len(all_activities)):
    a = mdl.integer_var(name= ("free activity: "+str(i)), domain= range(0, TIMESLOTS))
    all_activities.append(a)
    free.append(a)
    mdl.add(prev_a < a)
    prev_a = a

# add variables for each time slot
for i in range(TIMESLOTS):
    all_timeslots.append(mdl.integer_var(name=(DAYS[i//24] + " kl. " + str(i%24)), domain=range(0,len(all_activities))))

# set up channeling
mdl.add(mdl.inverse(all_activities,all_timeslots))

#-----------------------------------------------------------------------------
# Add constraints
#-----------------------------------------------------------------------------

#------------------
# Hard Mandatory
#------------------

# set timeslots for fixed activities
for i in range(len(fixed)):
    mdl.add(fixed[i] == fixed_times[i])

optionsbuilder.build(mdl,all_timeslots,ACTIVITIES,flex)

#-----------------------------------------------------------------------------
# Solve Model
#-----------------------------------------------------------------------------

msol = mdl.solve(TimeLimit=1000)

#-----------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------

if msol:
    print("Solution:")
    #solutionformatter.print_timeslots_to_console(msol,all_timeslots,all_activities)

    solutionformatter.print_non_empty_timeslots_to_console(msol,all_timeslots,all_activities,free)

    #solutionformatter.print_activities_to_console(msol,fixed,flex)

    #solutionformatter.print_non_activities_to_console(msol,free)

else:
    print("Solve status: " + msol.get_solve_status())
