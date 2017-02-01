__author__="Varun Rajiv Mantri"
import csv
import os
import statistics


def csvReader(fileName):
    startingLineFlag = 0
    file = open(fileName)
    fileread = csv.reader(file)
    print(fileName)
    return [fileread,file]

def inferenceBuilder(fileName1,fileName2):
    retrivedList=csvReader(fileName1)
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
    startingFlag=0
    dict={}
    for row in retrivedList[0]:
        userID=row[0]
        dict[userID]=0
        innerList=[0]
        if startingFlag==0:
            startingFlag=1
        else:
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
    #printing results
    return dict

def normalizerClassA(inputValue,referenceValue):
    temp = ((inputValue / referenceValue) * 100)
    temp=((temp/100)*25)
    return temp

def normalizerClassB(inputValue,referenceValue):
    temp = ((inputValue / referenceValue) * 100)
    temp=((temp/100)*10)
    return temp

def standardDeviationCal(dict):
    tempList=[]
    for key in dict:
        tempList.append(dict[key])
    std=statistics.stdev(tempList)
    return (std/3)

def matchFinder(dict,std):
    outPutDict={}
    lengthTempList = 0
    for key in dict:
        tempList=[]
        lowerBound=dict[key]-std
        upperBound=dict[key]+std
        for key2 in dict:
            if dict[key2]>lowerBound and dict[key2]<upperBound:
                tempList.append(key2)
        outPutDict[key]=tempList
        if len(tempList)>lengthTempList:
            lengthTempList=len(tempList)
    return [outPutDict,lengthTempList]

def csvWriter(outputDict):
    filePath = "D:\\intuit_challange\\rit-challenge\\transaction-data\\inferenceData"
    file = os.path.join(filePath, 'Solution.csv')
    file=open(file,'w+')
    for key in outputDict:
        file.write('SUBJECT ID:'+key+',')
        file.write('POSSIBLE MATCHES:,')
        for item in outputDict[key]:
            file.write(item+',')
        file.write('\n')

def main():
    filePath = "D:\\intuit_challange\\rit-challenge\\transaction-data\\inferenceData"
    file1=os.path.join(filePath, 'maxStorage.csv')
    file2=os.path.join(filePath, 'intermediateOutPut.csv')
    dict=inferenceBuilder(file1,file2)
    std=standardDeviationCal(dict)
    temp=matchFinder(dict,std)
    outputDict=temp[0]
    for key in outputDict:
        if key!='User ID':
            print('USER ID:'+key)
            print(outputDict[key])
            print('------------------')
    print('Output completed')
    csvWriter(outputDict)
main()