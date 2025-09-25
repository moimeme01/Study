import pandas as pd
import os
import course_calendar
from settings import *

actual_period = "Q1_2025_2026"

initial_path = '/Users/thibaultvanni/PycharmProjects/Study/' + actual_period
session_running_path = initial_path + "/session_running"
hours_done_path = initial_path + '/hours_done_' + actual_period

"""
Dans ce fichier nous créons de manièer automatique, si demandé, les fichiers qui contabiliseront les heures individuelles
des cours ainsi que les TP et les CM retravaillés. 

"""
actual_list_name = "Course_list_" + actual_period
all_dict = {}
for courses in getattr(course_calendar, actual_list_name):
    courseName = "".join(courses.split(" "))
    doneDictName = "Done"+ courseName

    # Attention a bien voir pour la longueur des semaines...

    values = {"CM":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0, "S14": 0},
              "TP":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0, "S14": 0}}
    all_dict[doneDictName] = values
    myvar = pd.DataFrame(all_dict[doneDictName])
    myvar.to_csv(initial_path + "/hours_done_" + actual_period + "/" + doneDictName + ".csv", mode='w', index=True, header=True)

    mydataset = {'Start': [],
                 'End': [],
                 'Delta': []}
    myvar = pd.DataFrame(mydataset)
    myvar.to_csv(initial_path + "/hours_done_" + actual_period + "/" + courseName + ".csv", mode='w', index=True, header=True)

