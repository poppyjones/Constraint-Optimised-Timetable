from docplex.cp.model import CpoModel
import timetableimporter
import optionsimporter
from definitions import TIMESLOTS, timeslot_to_string, SAT, SUN
from helperfunctions import get_timeslots_in_interval, get_timeslots_of_day

# Empty data structures for courses
class Course:
    def __init__(self, name):
        self.name = name
        self.fixed = []
        self.flex = []


class Model:
    def __init__(self, options_name, data_name, ACTIVITIES):
        self.name = "{}_options_{}".format(options_name, data_name)

        self.mdl = CpoModel()

        self.ACTIVITIES = ACTIVITIES
        # Empty activity data structures
        self.all_activities = []
        self.fixed = []
        self.flex = []
        self.other = []
        self.blocked = []
        self.free = []

        # Empty timeslot data structures
        self.all_timeslots = []*TIMESLOTS

        # Empty list for courses
        self.courses = []


def build():

    data_name, imported_courses, ACTIVITIES = timetableimporter.from_json()
    options_name, imported_options = optionsimporter.from_json()

    model = Model(data_name, options_name, ACTIVITIES)
    mdl = model.mdl

    domain = set(range(0, TIMESLOTS))

    for c_in in imported_courses:
        c = Course(c_in[0])
        model.courses.append(c)
        # fixed
        for fi in c_in[1]:
            a = mdl.integer_var(name=fi[0], domain=fi[1])
            domain.remove(fi[1])
            model.all_activities.append(a)
            model.fixed.append(a)
            c.fixed.append(a)
        # flex
        if(len(c_in[2]) > 1):
            a = mdl.integer_var(name=c_in[2].pop(
                0), domain=range(0, TIMESLOTS))
            model.all_activities.append(a)
            model.flex.append(a)
            c.flex.append(a)
            prev_a = a
            for fl in c_in[2]:
                a = mdl.integer_var(name=fl, domain=range(0, TIMESLOTS))
                model.all_activities.append(a)
                model.flex.append(a)
                c.flex.append(a)
                # break symmetry
                mdl.add(prev_a < a)
                prev_a = a
        else:
            for fl in c_in[2]:
                a = mdl.integer_var(name=fl, domain=range(0, TIMESLOTS))
                model.all_activities.append(a)
                model.flex.append(a)
                c.flex.append(a)

    # Add activity variables for other activities (out of school)
    for oa in imported_options.other_blocked:
        # don't add other activities if on same timeslot as a fixed activity
        if(oa[1] not in domain):
            print(f"conflicting activities on {timeslot_to_string(oa[1])}")
            continue
        a = mdl.integer_var(name=oa[0], domain=oa[1])
        model.all_activities.append(a)
        model.other.append(a)
        domain.remove(oa[1])

    # Add activity variable for blocked weekend timeslots
    if imported_options.remove_weekend == True:
        blocked_hours = get_timeslots_of_day(
            list(range(0, TIMESLOTS)), SAT) + get_timeslots_of_day(list(range(0, TIMESLOTS)), SUN)
        for h in blocked_hours:
            if h not in domain:
                continue
            a = mdl.integer_var(name="weekend", domain=h)
            model.all_activities.append(a)
            model.blocked.append(a)
            domain.remove(h)

    # Add activity variable for blocked sleep timeslots
    s0 = imported_options.sleep[0]
    s1 = imported_options.sleep[1]
    if(s0 != s1):
        blocked_hours = get_timeslots_in_interval(list(range(0, TIMESLOTS)), s0, s1)
        for h in blocked_hours:
            if h not in domain:
                continue
            a = mdl.integer_var(name="sleep", domain=h)
            model.all_activities.append(a)
            model.blocked.append(a)
            domain.remove(h)

    # Add variables for each free activity
    # - keeps them sorted to minimise nr. of solutions
    if(len(model.all_activities) < TIMESLOTS):
        prev_a = mdl.integer_var(name=("free activity: 0"), domain=domain)
        model.all_activities.append(prev_a)
        model.free.append(prev_a)

        for i in range(1, 1 + TIMESLOTS - len(model.all_activities)):
            a = mdl.integer_var(name=("free activity: "+str(i)), domain=domain)
            model.all_activities.append(a)
            model.free.append(a)
            # break symmetry
            mdl.add(prev_a < a)
            prev_a = a

    # add variables for each time slot
    for i in range(TIMESLOTS):
        model.all_timeslots.append(mdl.integer_var(
            name=timeslot_to_string(i), domain=range(0, len(model.all_activities))))

    # set up channeling
    mdl.add(mdl.inverse(model.all_activities, model.all_timeslots))

    return model, imported_options