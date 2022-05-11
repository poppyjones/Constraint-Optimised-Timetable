days_to_hrs = {"MON": (0*24),
            "TUE": (1*24),
            "WED": (2*24),
            "THU": (3*24),
            "FRI": (4*24),
            "SAT": (5*24),
            "SUN": (6*24)}
MON = "MON"
TUE = "TUE"
WED = "WED"
THU = "THU"
FRI = "FRI"
SAT = "SAT"
SUN = "SUN"
DAYS = [MON, TUE, WED, THU, FRI, SAT, SUN]
TIMESLOTS = len(DAYS)*24
WEEKEND = range(days_to_hrs["SAT"],TIMESLOTS)
def timeslot_to_day(t):
    return DAYS[t//24]
def timeslot_to_hr(t):
    return t%24
def timeslot_to_string(t):
    return f"{timeslot_to_day(t)}: {timeslot_to_hr(t)}".format(t)