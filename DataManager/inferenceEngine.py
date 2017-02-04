
"""
file: inferenceEngine.py
language: python3
author: Varun Rajiv Mantri
description: Code to classify users based on the gaussian distribution of their respective scores
OutPut: solution.csvv
"""

import csv
import os
import statistics
import matplotlib.pyplot as plt

def csvReader(fileName):
    '''
            csvReader reads a CSV file
                :param fileName: Complete path of subject file
                :return: list: list containing object of file and a handle to it (for closing)
    '''
    try :
        file = open(fileName)
        fileread = csv.reader(file)
    except IOError:
        print('Invalid address. Re-run the code with correct file address\n')
        return [-1,-1]
    #print(fileName)
    return [fileread,file]

def inferenceBuilder(fileName1,fileName2):
    '''
            inferenceBuilder contains the logic which evaluates different features and gives them score
                :param fileName1: file path of maxStorage.csv
                :param fileName2: file path of intermediateOutPut.csv
                :return: dict: dictionary where key is userID and value is user Score
    '''
    retrivedList=csvReader(fileName1)
    dict = {}
    if retrivedList[0]==-1 and retrivedList[1]==-1:
        dict['error']=-1
        return dict
    startingFlag=0
    maxCapacity=0
    maxStability=0
    maxFoody=0
    maxDrinking=0
    for row in retrivedList[0]:
        if startingFlag==0:
            startingFlag=1
        else:
            maxCapacity=float(row[0])
            maxStability=float(row[1])
            maxFoody=float(row[2])
            maxDrinking=float(row[3])
            maxRecreation=float(row[4])
    #closing the openned file
    retrivedList[1].close()
    retrivedList=csvReader(fileName2)
    startingFlag = 0
    for row in retrivedList[0]:
        if startingFlag==0:
            startingFlag=1
        else:
            userID = row[0]
            dict[userID] = 0
            #code for capacity
            temp=float(row[1])
            dict[userID]=dict[userID] + normalizerClassA(temp,maxCapacity)
            #code for stability
            temp = float(row[13])
            dict[userID] = dict[userID] + normalizerClassA(temp, maxStability)
            #code for childern
            if row[7]=='YES':
                dict[userID]=dict[userID] + 12.5
            else:
                dict[userID] = dict[userID]+ 25
            #code for divorced
            if row[11] == 'NO':
                dict[userID] = dict[userID] + 25
            else:
                dict[userID]= dict[userID] + 12.5
            #code for foodyness
            temp=float(row[2])
            dict[userID] = dict[userID] + normalizerClassB(temp, maxFoody)
            #code for drinker
            temp = float(row[4])
            dict[userID] = dict[userID] + normalizerClassB(temp, maxDrinking)
            #code for recreation
            temp= float(row[5])
            dict[userID] = dict[userID] + normalizerClassB(temp, maxRecreation)
            #code for pet
            if row[10]=='YES':
                dict[userID] = dict[userID] + 10
            else:
                dict[userID] = dict[userID] + 0
            dict[userID] = ((dict[userID]/140)*100)
    #printing results
    return dict

def normalizerClassA(inputValue,referenceValue):
    '''
            normalizerClassA compares inputValue against referenceValue and builds a score out 25
                :param inputValue: the value which is to be normalized
                :param referenceValue: value against which inputValue is normalized
                :return: list: normalized value
    '''
    temp = ((inputValue / referenceValue) * 100)
    temp=((temp/100)*25)
    return temp

def normalizerClassB(inputValue,referenceValue):
    '''
            normalizerClassB compares inputValue against referenceValue and builds a score out 10
                :param inputValue: the value which is to be normalized
                :param referenceValue: value against which inputValue is normalized
                :return: list: normalized value
    '''
    temp = ((inputValue / referenceValue) * 100)
    temp=((temp/100)*10)
    return temp

def standardDeviationCal(dict):
    '''
            standardDeviation calculates standard deviation and mean of all the values in dict
                :param dict: the dictionary of which standard deviation and mean has to be calculated
                :return: list: list of standard deviation and mean
    '''
    tempList=[]
    for key in dict:
        tempList.append(dict[key])
    std=statistics.stdev(tempList)
    mn=statistics.mean(tempList)
    return [std,mn]

def matchFinder(dict,std,mn):
    '''
            matchFinder classifies the users into 5 distinct groups using Gaussian distribution
            individuals in this group are the people with relatively similar scores which indicates their mutual
            compatibility
                :param dict: dictionary where key is userID and value is user Score
                :param std: standard deviation of all the scores in 'dict'
                :param mn: mean of all the scores in dict
                :return: outPutDict: dictionary where key is groupID and value is list of people(users) with similar scores
    '''
    outPutDict={}
    lengthTempList = 0
    grp1=[]
    grp2=[]
    grp3=[]
    grp4=[]
    grp5=[]
    for key in dict:
        val=dict[key]
        if (val>mn and val < mn+std/2) or (val<mn and val>(mn-std/2)):
            grp1.append(key)
        elif val>(mn+std/2) and val<(mn+3*std/2):
            grp2.append(key)
        elif val>(mn+3*std/2):
            grp3.append(key)
        elif val < (mn - std/2) and val > (mn -( 3*std/2)):
            grp4.append(key)
        elif val < (mn - (3*std/2)):
            grp5.append(key)
    outPutDict['Group 1 (-.5*sigma to 0.5*sigma)']=grp1
    outPutDict['Group 2(0.5*sigma to 1.5*sigma)']=grp2
    outPutDict['Group 3(1.5*sigma to infinity)']=grp3
    outPutDict['Group 4(-0.5*sigma to -1.5*sigma)'] = grp4
    outPutDict['Group 5 (-1.5*sigma to infinity)'] = grp5
    return [outPutDict,lengthTempList]

def csvWriter(outputDict,filePath):
    '''
            csvWriter writes the contents of outPutDict to a csv file
                :param outPutDict: dictionary where key is groupID and value is list of people(users) with similar scores
    '''
    #filePath = "D:\\intuit_challange\\rit-challenge\\transaction-data\\inferenceData"
    file = os.path.join(filePath, 'Solution.csv')
    file=open(file,'w+')
    for key in outputDict:
        file.write(str(key) +':,')
        for item in outputDict[key]:
            file.write(item+',')
        file.write('\n')

def graphPlotter(dict):
    '''
            Plots the histogram using the data in dictionary dict
                :param dict: dictionary where key is userID and value is user Score
    '''
    values=[]
    for key in dict:
        values.append(dict[key])
    plt.hist(values)
    plt.title('SCORE DISTRIBUTION')
    plt.xlabel('SCORES')
    plt.ylabel('Frequency of occurrence')
    plt.show()

def start(filePath):
    '''
            start function for inferenceEngine
                :param filePath: path where results of featureExtracter.py are stored
    '''
    file1 = os.path.join(filePath, 'maxStorage.csv')
    file2 = os.path.join(filePath, 'intermediateOutPut.csv')
    dict = inferenceBuilder(file1, file2)
    if 'error' in dict.keys():
        return -1
    retList = standardDeviationCal(dict)
    std = retList[0]
    mn = retList[1]
    temp = matchFinder(dict, std, mn)
    outputDict = temp[0]
    #print(outputDict)
    csvWriter(outputDict,filePath)
    decision=input('Would you like to see histogram showing distribution of users scores? \nenter y to do so..... else enter any other letter to continue. \n(note - after viewing histogram, please close its window to proceed to next part of code.)')
    if decision=='y':
        graphPlotter(dict)
    while True:
        user1=input('Enter User ID of 1st individual:')
        user2=input('Enter User ID of 2nd individual:')
        flag=0
        try :
            val1= dict[user1]
            val2 = dict[user2]
            flag=1
        except KeyError:
            print('Invalid User-ID ')
        if flag==1:
            print('Score : '+str(1-(abs(val1-val2)/100)))
        code=input('Enter q to exit or enter any other letter to proceed\n')
        if code=='q':
            break
    return 1

def main():
    filePath=input('Enter the path where results of featureExtracter.py are stored:')
    #filePath = "D:\\intuit_challange\\rit-challenge\\transaction-data\\inferenceData"
    val=start(filePath)
    if val==1:
        print('Execution completed.....\n')
    else:
        print('Execution aborted.....\n')


if __name__=='__main__':
    main()