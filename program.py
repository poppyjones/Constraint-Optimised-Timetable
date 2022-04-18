from docplex.cp.model import CpoModel
import solutionformatter
import timetableimporter
import constraintbuilder
import optionsimporter
from definitions import TIMESLOTS, DAYS

#-----------------------------------------------------------------------------
# Initialize the problem data
#-----------------------------------------------------------------------------

imported_courses, ACTIVITIES = timetableimporter.from_json()

# Empty activity data structures
all_activities = []
fixed = []
flex  = []
free = []

# Empty timeslot data structures
all_timeslots = []*TIMESLOTS

# Empty data structures for courses
class Course:
    def __init__(self, name):
        self.name = name
        self.fixed = []
        self.flex = []

courses = []


#-----------------------------------------------------------------------------
# Build the model
#-----------------------------------------------------------------------------

# Create model
mdl = CpoModel()

for c_in in imported_courses:
    c = Course(c_in[0])
    courses.append(c)
    # fixed
    for fi in c_in[1]:
        a = mdl.integer_var(name= fi[0], domain= fi[1])
        all_activities.append(a)
        fixed.append(a)
        c.fixed.append(a)
    #flex
    if(len(c_in[2])>1):
        a = mdl.integer_var(name= c_in[2].pop(0), domain= range(0, TIMESLOTS))
        all_activities.append(a)
        flex.append(a)
        c.flex.append(a)
        prev_a = a
        for fl in c_in[2]:
            a = mdl.integer_var(name= fl, domain= range(0, TIMESLOTS))
            all_activities.append(a)
            flex.append(a)
            c.flex.append(a)
            #break symmetry
            mdl.add(prev_a < a)
            prev_a = a
    else:
        for fl in c_in[2]:
            a = mdl.integer_var(name= fl, domain= range(0, TIMESLOTS))
            all_activities.append(a)
            flex.append(a)
            c.flex.append(a)

# Add variables for each free activity
# - assumes at least one empty slot
# - keeps them sorted to minimise nr. of solutions
prev_a = mdl.integer_var(name= ("free activity: 0"), domain= range(0, TIMESLOTS))
all_activities.append(prev_a)
free.append(prev_a)

for i in range(1,1 + TIMESLOTS - len(all_activities)):
    a = mdl.integer_var(name= ("free activity: "+str(i)), domain= range(0, TIMESLOTS))
    all_activities.append(a)
    free.append(a)
    # break symmetry
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

constraintbuilder.build(mdl,all_timeslots,ACTIVITIES,flex,courses)

#-----------------------------------------------------------------------------
# Solve Model
#-----------------------------------------------------------------------------

msol = mdl.solve(TimeLimit=120)

#-----------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------

if msol:
    print("Solution:")
    solutionformatter.create_html_timetable(msol,courses)

else:
    print("Solve status: " + msol.get_solve_status())
