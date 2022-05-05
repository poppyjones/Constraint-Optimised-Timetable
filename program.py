import solutionformatter
import constraintbuilder
import modelbuilder

#-----------------------------------------------------------------------------
# Initialize the model
#-----------------------------------------------------------------------------

model, imported_options = modelbuilder.build()

#-----------------------------------------------------------------------------
# Add constraints
#-----------------------------------------------------------------------------

constraintbuilder.build(model, imported_options)

#-----------------------------------------------------------------------------
# Solve Model
#-----------------------------------------------------------------------------

msol = model.mdl.solve(TimeLimit=10)

#-----------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------

if msol:
    print("Solution:")
    solutionformatter.print_activities_to_console(msol,model.fixed,model.flex)
    solutionformatter.create_html_timetable(msol,model.name,model.courses,model.other)

else:
    print("Solve status: " + msol.get_solve_status())
