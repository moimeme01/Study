import pandas as pd
import os
os.makedirs("/Users/thibaultvanni/PycharmProjects/Study/hours_done", exist_ok=True)



DoneThermodynamique = {"CM":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0},
                       "TP":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0}}
myvar = pd.DataFrame(DoneThermodynamique)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/DoneThermodynamique.csv', mode='w', index=True, header=True)

DoneFabrimeca = {"CM":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0},
                 "TP":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0}}
myvar = pd.DataFrame(DoneFabrimeca)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/DoneFabricationMécanique.csv', mode='w', index=True, header=True)

DoneTelecomunication = {"CM":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0},
                        "TP":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0}}
myvar = pd.DataFrame(DoneTelecomunication)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/DoneTélécommunications.csv', mode='w', index=True, header=True)

DoneMMC ={"CM":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0},
          "TP":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0}}
myvar = pd.DataFrame(DoneMMC)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/DoneMécaniquedesMilieuxContinus.csv', mode='w', index=True, header=True)

DoneTEST = {"CM":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0},
                        "TP":{"S1": 0, "S2": 0,"S3": 0,"S4": 0,"S5": 0,"S6": 0,"S7": 0,"S8": 0,"S9": 0,"S10": 0,"S11": 0,"S12": 0,"S13": 0}}
myvar = pd.DataFrame(DoneTEST)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/DoneTEST.csv', mode='w', index=True, header=True)








mydataset = {'Start': [],
             'End': [],
             'Delta': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/FabricationMécanique.csv', mode='w', index=True, header=True)

mydataset = {'Start': [],
             'End': [],
             'Delta': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/MécaniquedesMilieuxContinus.csv', mode='w', index=True, header=True)


mydataset = {'Start': [],
             'End': [],
             'Delta': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/Télécommunications.csv', mode='w', index=True, header=True)


mydataset = {'Start': [],
             'End': [],
             'Delta': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/Thermodynamique.csv', mode='w', index=True, header=True)

mydataset = {'Start': [],
             'End': [],
             'Delta': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/TEST.csv', mode='w', index=True, header=True)

mydataset = {'Start': [],
             'Delta': []}
myvar = pd.DataFrame(mydataset)
myvar.to_csv('/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv', mode='w', index=True, header=True)
