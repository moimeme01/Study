import pandas as pd
import os
import course_calendar
from create_total_file import *
from main import initial_path, actual_period


mydataset = []
actual_list_name = "Course_list_" + actual_period

for courses in getattr(course_calendar, actual_list_name):
    name = "".join(courses.split(" "))
    TPNumber = 0
    CMNumber = 0
    for key in getattr(course_calendar, name).keys():
        CMNumber += getattr(course_calendar, name)[key].count("CM")
        TPNumber += getattr(course_calendar, name)[key].count("TP")
    for i in range(1, TPNumber + 1):
        mydataset.append([courses, "TP", f"TP{i}", "NO"])
    for i in range(1, CMNumber+1):
        mydataset.append([courses, "CM", f"CM{i}", "NO"])

mydataset = pd.DataFrame(mydataset, columns=["Course", "Type", "Session", "Done"])
mydataset.to_csv(initial_path + "TPCMNUMBERS.csv", mode='w', index=False)


