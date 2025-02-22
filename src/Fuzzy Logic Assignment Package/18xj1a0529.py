# -*- coding: utf-8 -*-
"""18xj1a0529.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1plqNnbopOeoMCeP9T0RA7i8DXtLb0zh-
"""

import pandas as pd
import numpy as np


def degOfBel(inp):
    boundaries = [-0.66, -0.33, 0, 0.15, 0.33, 0.45, 0.75]
    degofbel = [0 for i in range(len(boundaries))]
    if inp < boundaries[0]:
        degofbel[0] = 1
    elif inp > boundaries[-1]:  # These are corner cases that do not have any overlapping
        # sets, so an input fully belongs to the corner set.
        degofbel[-1] = 1
    else:
        for i in range(len(boundaries) - 1):
            if inp >= boundaries[i] and inp < boundaries[i + 1]:
                degofbel[i + 1] = (inp - boundaries[i]) / \
                    (boundaries[i+1] - boundaries[i])
                degofbel[i] = (boundaries[i + 1] - inp) / \
                    (boundaries[i+1] - boundaries[i])
                break
    return degofbel


def Defuzzify(dob1, dob2, fam):
    dob1t = np.array(dob1)
    dob2t = np.array(dob2)
    dob1t = dob1t.reshape(-1, 1)
    dob2t = dob2t.reshape(1, -1)
    den = 0
    num = 0
    intensityweights = dob1t @ dob2t
    for i in range(len(intensityweights)):
        for j in range(len(intensityweights[0])):
            num = num + intensityweights[i][j]*fam[i][j]
            den = den + intensityweights[i][j]
            
    print(num, den)
    z = num/den
    return z


def subCentroids(fam):
    finalFam = []
    for sections in fam:
        section = []
        for subsets in sections:
            if (subsets == 1):
                section.append(-0.75)
            elif (subsets == 2):
                section.append(0)
            elif (subsets == 3):
                section.append(0.2)
            elif (subsets == 4):
                section.append(0.4)
            elif (subsets == 5):
                section.append(0.5)
            elif (subsets == 6):
                section.append(0.6)
            elif (subsets == 7):
                section.append(0.7)
            elif (subsets == 8):
                section.append(0.8)
            elif (subsets == 9):
                section.append(0.95)
        finalFam.append(section)
    finalFam = np.array(finalFam)
    return finalFam


inpt = pd.read_csv(r"input.csv")  # please provide your absolute path here
inp = inpt.drop(["Case No."], axis=1)
# Storing x1 and x2 in an array
x1inp = inp["x1 (°C/sec)"].to_numpy()
x2inp = inp["x2 (°C)"].to_numpy()

# initialising extremes from domain
x1max = 10
x1min = -10
x2max = 30
x2min = -30

# Normalizing
x1_ninp = [round((inputs*2 - (x1max + (x1min)))/(x1max-(x1min)), 3)
           for inputs in x1inp]
x2_ninp = [round((inputs*2 - (x2max + (x2min)))/(x2max-(x2min)), 3)
           for inputs in x2inp]

# Fuzzification
degofbel_x1_ninp = [degOfBel(num) for num in x1_ninp]
degofbel_x2_ninp = [degOfBel(num) for num in x2_ninp]

#print(np.array(degofbel_x1_ninp), "\n", np.array(degofbel_x2_ninp))

# Defining FAM
FAM = np.array([[1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 2],
                [1, 1, 1, 1, 1, 1, 3],
                [1, 1, 1, 1, 2, 3, 5],
                [1, 1, 1, 2, 2, 4, 6],
                [1, 1, 2, 3, 4, 6, 8],
                [1, 2, 3, 5, 6, 8, 9]])

FAM = subCentroids(FAM)

print(FAM)

# Defuzzification to produce a crisp output
res = []
for i in range(len(degofbel_x1_ninp)):
    # Results and their denormalisation to [0, 100]
    res.append(
        round(50*(1 + Defuzzify(degofbel_x1_ninp[i], degofbel_x2_ninp[i], FAM)), 3))

inpt["Breakoutablity"] = res

inpt.to_csv("output.csv", index=False)

print("output.csv: ", inpt)
