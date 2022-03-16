
days_to_nr = {"MON": 0,
            "TUE": 1,
            "WED": 2,
            "THU": 3,
            "FRI": 4,
            "SAT": 5,
            "SUN": 6}
days_to_hrs = {"MON": 0,
             "TUE": (1*24),
             "WED": (2*24),
             "THU": (3*24),
             "FRI": (4*24),
             "SAT": (5*24),
             "SUN": (6*24)}
DAYS = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
TIMESLOTS = len(DAYS)*24
WEEKEND = range(days_to_hrs["SAT"],TIMESLOTS)