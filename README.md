# Constraint-Optimised-Timetable

This program was developed as part of a Bachelors Thesis at the IT University of Copenhagen.

## How to run

Run `python program.py`, the program will prompt you for a time table (the fixed activities scheduled by a university) and options (the users personal preferences). The former can be found in `.\data\` folder, the latter in `.\options\`. To create your own user preferences, you can use the template found in the same folder. The resulting timetable will be created as an `html` file in the `.\output\` folder.

Note that to use the constraint solver, you must have access to the IBM ILOG CPLEX Optimization Studio.
