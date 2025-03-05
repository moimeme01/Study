import pandas as pd
import os
import course_calendar
from course_calendar import Course_list

Thermodynamique = {"S1": ["CM"],
                   "S2": ["TP", "CM"],
                   "S3": ["TP", "CM"],
                   "S4": ["TP", "CM"],
                   "S5": ["TP", "CM"],
                   "S6": ["TP", "CM"],
                   "S7": ["TP", "CM"],
                   "S8": ["TP", "CM"],
                   "S9": ["TP", "CM"],
                   "S10": ["TP", "CM"],
                   "S11": ["TP", "CM"],
                   "S12": ["TP", "CM"],
                   "S13": ["TP", "CM"]}


mydataset = {'Course': [],
             'End': [],
             'Delta': [],
             'Course': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/TPCMNUMBERS.csv', mode='w', index=True, header=True)

total = pd.read_csv("/Users/thibaultvanni/PycharmProjects/Study/hours_done/TPCMNUMBERS.csv")

for courses in Course_list:
    TPNumber = 0
    CMNumber = 0
    for key in getattr(course_calendar, courses).keys():
        CMNumber += getattr(course_calendar, courses)[key].count("CM")
        TPNumber += getattr(course_calendar, courses)[key].count("TP")




