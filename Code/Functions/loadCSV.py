# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 15:59:28 2020

@author: Lyle Regenwetter (regenwet@mit.edu)
"""
import csv
from os import path
import numpy as np
import sys

def loadCSV():
    enableProgressBar=1
    #Progress Bar code
    if enableProgressBar==1:
        toolbar_width = 40
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
    
    #Initializations
    featureDict={}
    numFeatures=0
    numModels=4800
    csvUnassigned=1
    anomalyLog=''
    # modelIncrement=0
    
    #Loop over models
    for modelNum in range(1,numModels):
        csvPath='..\\CSVs\\'
        csvName=csvPath+"(" + str(modelNum) + ").csv"
        rowCount=0
        if path.exists(csvName): #If file exists
            with open(csvName, newline='', encoding="utf8") as csvFile:
                readCsv=csv.reader(csvFile, delimiter=',')
                for row in readCsv: #Loop over rows of CSV
                    if (rowCount>1):
    
                        #Debugging catch
    #                     if numModels==1036:
    #                         print(row)
                        
                        skip=0
                        
                        #Anomaly catch #0
                        if (len(row)>7 or len(row)<=2) and skip==0:
                            skip=1
                            row=['']*(6)
                            anomalyLog=anomalyLog + "Catch 0 on model " + str(modelNum) + " on row " + str(rowCount) + "\n"    
                           
                        #Anomaly catch #1
                        if (row[2]=="Driving" or row[2]=="Driven") and skip==0:
                            skip=1
                            anomalyLog=anomalyLog + "Catch 1 on model " + str(modelNum) + " on row " + str(rowCount) + "\n"
                        #Anomaly catch #2
                        if len(row)<6 and skip==0:
                            row=row+(['']*(6-len(row)))
                            anomalyLog=anomalyLog + "Catch 2 on model " + str(modelNum) + " on row " + str(rowCount) + "\n"    
                        #Anomaly catch #3
                        if len(row)==7 and skip==0:
                            row[3:5]=row[4:6]
                            del row[6]
                            anomalyLog=anomalyLog + "Catch 3 on model " + str(modelNum) + " on row " + str(rowCount) + "\n"    
                          
                        feature=tuple([row[0], row[1]])                           
                        if feature in featureDict and skip==0: #If particular feature has been seen before
                            featureIndex=featureDict[feature]
                            while (len(csvData[featureIndex])<modelNum): #Fill in blanks until index maches current
                                csvData[featureIndex].append(['','','',''])
                            if len(csvData[featureIndex])==modelNum: #Ensure Duplicate features in a model arent rerecorded
                                vals=[row[2], row[3], row[4], row[5]]
                                csvData[featureIndex].append(vals)
    
                        elif skip==0: #If particular feature has never been encountered
                            featureDict[feature]=numFeatures
                            featureIndex=numFeatures
                            numFeatures+=1
                            empty=np.full([modelNum-1,4], '').tolist() #Need to add empty cells for all previous models
                            empty.append([row[2], row[3], row[4], row[5]])
                            
                            if csvUnassigned: #If this is the absolute first entry
                                csvData=[empty]
                                csvUnassigned=0
                            else:
                                csvData.append(empty)     
                    rowCount+=1
    
    
    #More progress bar code
            if enableProgressBar==1:
                sys.stdout.write("-")
                sys.stdout.flush()
    if enableProgressBar==1:
        sys.stdout.write("]\n")
        
    for i in range(len(csvData)):
#         print(len(csvData[i]))
#         print(numModels-len(csvData[i]))
        empty=np.full([numModels-len(csvData[i]),4], '').tolist()
        csvData[i].extend(empty)
        
        csvData[i]=[(list(featureDict.keys())[list(featureDict.values()).index(i)]),csvData[i]]
        
    
    return (csvData, anomalyLog)