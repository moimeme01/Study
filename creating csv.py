import pandas as pd
import os
import course_calendar
from main import initial_path, actual_period

"""
Dans ce fichier nous créons de manièer automatique, si demandé, les fichiers qui contabiliseront les heures individuelles
des cours ainsi que les TP et les CM retravaillés. 

"""
actual_list_name = "Course_list_" + actual_period
os.makedirs("/Users/thibaultvanni/PycharmProjects/Study/hours_done", exist_ok=True)
all_dict = {}
for courses in getattr(course_calendar, actual_list_name):
    doneDictName = "Done"+ courses

    # Attention a bien voir pour la longueur des semaines...

    values = {"CM":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0, "S14": 0},
              "TP":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0, "S14": 0}}
    all_dict[doneDictName] = values
    myvar = pd.DataFrame(all_dict[doneDictName])
    myvar.to_csv(initial_path + '/' + doneDictName + '.csv', mode='w', index=True, header=True)

    mydataset = {'Start': [],
                 'End': [],
                 'Delta': []}
    myvar = pd.DataFrame(mydataset)
    myvar.to_csv(initial_path + '/' + courses + '.csv', mode='w', index=True, header=True)

