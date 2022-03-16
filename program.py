from docplex.cp.model import CpoModel
import solutionformatter
import timetableimporter
from definitions import WEEKEND, TIMESLOTS

#-----------------------------------------------------------------------------
# Initialize the problem data
#-----------------------------------------------------------------------------

activity_names, fixed_times = timetableimporter.from_json()

# Empty data structures
all = []
fixed = []
flex  = []


#-----------------------------------------------------------------------------
# Build the model
#-----------------------------------------------------------------------------

# Create model
mdl = CpoModel()

# Add activities
for i in range(len(activity_names)):
    a = mdl.integer_var(name= activity_names[i], domain= range(0, TIMESLOTS))
    all.append(a)

    if i < len(fixed_times):
        fixed.append(a)
    else:
        flex.append(a)

# set timeslots for fixed activities
for fi in fixed:
    mdl.add( fi == fixed_times[i])

# no activities with the same timeslots
mdl.add(mdl.all_diff(all))


#-----------------------------------------------------------------------------
# Add constraints
#-----------------------------------------------------------------------------

# Hard no weekend

for fl in flex:
    mdl.add( fl != n for n in WEEKEND)

# min/max weekend

#-----------------------------------------------------------------------------
# Solve Model
#-----------------------------------------------------------------------------

msol = mdl.solve(TimeLimit=10)

#-----------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------

solutionformatter.print_to_console(fixed,flex,msol)