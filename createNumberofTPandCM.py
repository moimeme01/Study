import pandas as pd
import os
import course_calendar
from course_calendar import Course_list



mydataset = []

for courses in Course_list:
    TPNumber = 0
    CMNumber = 0
    for key in getattr(course_calendar, courses).keys():
        CMNumber += getattr(course_calendar, courses)[key].count("CM")
        TPNumber += getattr(course_calendar, courses)[key].count("TP")
    for i in range(1, TPNumber + 1):
        mydataset.append([courses, "TP", f"TP{i}", "NO"])
    for i in range(1, CMNumber+1):
        mydataset.append([courses, "CM", f"CM{i}", "NO"])

mydataset = pd.DataFrame(mydataset, columns=["Course", "Type", "Session", "Done"])
mydataset.to_csv('/Users/thibaultvanni/PycharmProjects/Study/TPCMNUMBERS.csv', mode='w', index=False)
test = pd.read_csv("/Users/thibaultvanni/PycharmProjects/Study/TPCMNUMBERS.csv")


