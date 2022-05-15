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

msol = model.mdl.solve(SearchType="Auto",TimeLimit=60)

#-----------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------

if msol:
    print("Solution:")
    #solutionformatter.append_solution(model.name,msol)
    solutionformatter.create_html_timetable(msol,model.name,model.courses,model.other)

else:
    print("Solve status: " + msol.get_solve_status())
