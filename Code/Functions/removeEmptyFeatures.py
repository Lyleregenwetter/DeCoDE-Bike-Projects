# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:24:27 2020

@author: Lyle Regenwetter (regenwet@mit.edu)
"""

def removeEmptyFeatures(csvData):
    empties=[]
    for i in range(len(csvData)):
        content=0
        for j in range(len(csvData[i][1])):
            if (csvData[i][1][j][2]!='' and csvData[i][1][j][2]!='N/A'):
                content=1
        if (content==0):
            empties.insert(0,i)
    for i in empties:
        del csvData[i]
    return csvData  