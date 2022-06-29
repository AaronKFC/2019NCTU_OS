import numpy as np
import pandas as pd

'''Load the data to build file lists'''
cltA = pd.read_csv('clientA.csv',header=None)
cltA = cltA.values
cltB = pd.read_csv('clientB.csv',header=None)
cltB = cltB.values

race_condi = []
for a in range(len(cltA)):
#    for b in range(len(cltB)):
    if cltA[a] == cltB[a]:
           race_condi.append(cltA[a])

#for i in range(len(race_condi)):
#    if race_condi[i] == 35932:
#        print(race_condi[i])
        
