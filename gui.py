import urllib


def begin_table():
    return '<table id="timetable"><tr><th>Hours</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th><th>Sunday</th>'


def end_table():
    return "</td></tr></table>"


def new_row(s=""):
    return '</tr><tr class="{}">'.format(s)


def build_timetable(timetable):
    html = begin_table()

    for i in range(len(timetable)):
        html += new_row()
        html += "<td class='hours'>{}</td>".format(str(i)+":00")
        for j in range(len(timetable[0])):
            timeslot = timetable[i][j]
            if timeslot:
                html += "<td class='{}'>{}</td>".format(
                    timeslot[0], timeslot[1])
            else:
                html += "<td class='empty'></td>"

    html += end_table()
    return html


def begin_document(title="Time Table solution"):
    return """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><meta charset="utf-8"><link rel="stylesheet" href="style.css"><title>{0}</title></head><body><h1>{0}</h1>""".format(title)


def end_document():
    return "</html>"


def build_output_gui(name, timetable):
    html = begin_document(name)
    html += build_timetable(timetable)
    html += end_document()

    filename = f"output/{name}.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

