
"""
file: featureExtracter.py
language: python3
author: Varun Rajiv Mantri
description: code to extract distinct features from Mint data present in a CSV file
OutPut: maxStorage.csv, intermediateSolution.csv
"""


import csv
import os

def csvReader(fileName):
    '''
        csvReader reads a CSV file
            :param fileName: Complete path of subject file
            :return: list: list containing object of file and a handle to it (for closing)
    '''
    startingLineFlag = 0
    try:
        file = open(fileName)
        fileread = csv.reader(file)
    except IOError:
        print('Invalid address. Re-run the code with correct file address')
        return [-1, -1]
    print(fileName)
    return [fileread,file]

def initializationCode():
    '''
        code that initializes lists with keywords and features
            :return: list: list contains two lists, one that contains the names of the actual features and one that contains keywords/phrases
    '''
    keyWordList = table = [None for _ in range(1000)]
    featureList = ['User ID','Financial Capacity', 'Food', 'Transportation', 'Drinking', 'Recreation', 'House?','parent?', 'student?', 'car?','pet?','Divorced?','Expenditure post paycheck','Financial stability']
    tempList = [['Public Transportation', 3], ['Restaurant', 2], ['Taxi', 3], ['Uber', 3], ['Bar', 4],['Foods',2],
                ['Night Club', 4], ['Inn', 5], ['Brewery', 4],['Wine',4], ['Housing Rent', 6], ['Pet',10],['Divorce',11],['Online Education Courses',8],['Student',8],['Babies',7],['Bowling',5],['Movie Ticket',5],['Concert',5],['Ice Skating Rink',5],['Museum',5]]
    plist=[]
    for item in tempList:
        index = hash(item[0]) % 1000
        collision=0
        if keyWordList[index]!=None:
            collision=collision+1
        plist.append(index)
        keyWordList[index] = item
    print(collision)
    return  [keyWordList,featureList]

def featureExtracter(fileName):
    '''
        featureExtracter extracts the actual features from input file
            :param fileName: subject file
            :return:  List containing list that contains the labels for extracted features and list that corresponds one to
            one with the earlier list
    '''
    List=initializationCode()
    keyWordList=List[0]
    featureList=List[1]
    fileRead=csvReader(fileName)
    file=fileRead[0]
    startingLineFlag = 0
    totalSpending=0
    income=0
    featureData=[0 for _ in range(14)]
    uId=0
    paycheckCounter=0
    flag=0
    for row in file:
        if startingLineFlag == 0:
            startingLineFlag = 1
        else:
            uId=row[0]
            stringline=row[2]
            wordList=stringline.split()
            #code for computing total income
            #-------------------------------
            if row[2]=='Paycheck':
                income=income+float(row[3])
                paycheckCounter=paycheckCounter+1
                #flag raised to initiate spending counting
                flag=1
            #-------------------------------
            retVal=helperExtracter(wordList,keyWordList)
            if retVal[0]==True:
                featureData[int(retVal[1])]=featureData[int(retVal[1])]+(-1*float(row[3]))
            #calculations for totalIncome
            tempVal=float(row[3])
            if tempVal<0 and flag==1:
                totalSpending=totalSpending+tempVal
    featureData=inferenceBuilder(featureData,income)
    #annualIncome=totalIncome(fileName)
    if paycheckCounter==0:
        featureData[1]=0
        featureData[13] = 0
        featureData[13] = 0
    else:
        featureData[1]=(income/paycheckCounter)  #gives avg-income
        featureData[13] = (income / (-1 * totalSpending))
        featureData[12]=(-1*totalSpending)
    featureData[0]=uId
    fileRead[1].close()
    #testing
    print(featureList)
    print(featureData)
    return [featureList,featureData]


def inferenceBuilder(featureData,totalincome):
    '''
            inferencebuilder builds first order inference where if a value is greater than certain value, it's written as 'YES' else 'NO'
            (applicable to only certain features)
                :param featureData: list that corresponds to the list of features
                :param totalincome: total earnings
                :return: featureData: list that corresponds to the list of features
    '''
    # converting to percentage and building inference
    referenceList = [2, 3, 4, 5, 10]
    if totalincome != 0:
        for item in referenceList:
            temp = float(featureData[item])
            featureData[item] = ((temp / totalincome) * 100)
    referenceList = [6, 7, 8, 10, 11]
    for item in referenceList:
        if featureData[item] > 0 and item != 6:
            featureData[item] = 'YES'
        elif item == 6 and featureData[item] > 0:
            featureData[item] = 'NO'
        elif item==6 and featureData[item]==0:
            featureData[9]='YES'
        else:
            featureData[item] = 'NO'
    if featureData[3]>0:
        featureData[9]='NO'

    return featureData

def fileWriter(file,featureList,featureData):
    '''
            writes to a file
                :param file: name of the file to which data is to be written
                :param featureList: list that contains the labels for extracted features
                :param featureData:  list that corresponds to the list of features (i.e. featureList)
                :return: featureData: list that corresponds to the list of features
    '''
    if featureList!=-1:
        for item in featureList:
            file.write(str(item)+',')
        file.write('\n')
    for item in featureData:
        file.write(str(item)+',')
    file.write('\n')

def maxValuesWriter(file,maxCapacity,maxStability,maxFoody,maxDrinking,maxRecreation):
    '''
            writes to a file
                :param file: name of the file to which data is to be written
                :param maxCapacity: one of the feature
                :param maxStability: one of the feature
                :param maxFoody: one of the feature
                :param:maxDrinking: one of the feature
                :param:maxRecreation: one of the feature
    '''
    file.write('MaxCapacity,MaxStability,maxFoodyness,maxDrinking,maxRecreation\n')
    file.write(str(maxCapacity)+','+str(maxStability)+','+str(maxFoody)+','+str(maxDrinking)+','+str(maxRecreation)+'\n')

def helperExtracter(wordList,keyWordList):
    '''
            helper function for featureExtracter
                :param wordList: list of words generated from the phrase extracted from input CSV file
                :param keyWordList:list of keywords stored as default list for this program
                :return:List of boolean value
    '''
    length=len(wordList)-1
    counter=0
    currentItem=''
    foundFlag=0
    baseCounter=0
    currentItem = wordList[counter]
    while baseCounter<=length:
        startFlag = 0
        while counter<length and foundFlag!=1:
            if startFlag==0:
                currentItem = wordList[baseCounter]
                startFlag=1
            else:
                counter = counter + 1
                #print(baseCounter)
                currentItem = currentItem + ' ' + wordList[counter]
            index=hash(currentItem)%1000
            tempkey=keyWordList[index]
            if tempkey!=None and tempkey[0]==currentItem:
                foundFlag=1
            elif baseCounter==length:
                break
        if foundFlag==1:
            return [True,tempkey[1]]
        baseCounter=baseCounter+1
        counter=baseCounter
    return [False,None]

def start(filePath,directoryPath):
    '''
            wstart function for featureExtracter.py
                :param filePath: path where the target files will be generated
                :param directoryPath: path of directory from where user data is to be read
    '''
    completeName = os.path.join(filePath, 'intermediateOutPut.csv')
    try:
        outputFile = open(completeName, 'w+')
    except IOError:
        print('Invalid path!')
        return -1
    startingFlag = 0
    # Storing the maximum values in file
    maxCapacity = 0
    maxStability = 0
    maxFoody = 0
    maxDrinking = 0
    maxRecreation = 0
    for file in os.listdir(directoryPath):
        if file.endswith('.csv'):
            print(file)
            finalList = featureExtracter(file)
            if startingFlag == 0:
                fileWriter(outputFile, finalList[0], finalList[1])
                tempList = finalList[1]
                maxCapacity = float(tempList[1])
                maxStability = float(tempList[13])
                maxFoody = float(tempList[2])
                maxDrinking = float(tempList[4])
                maxRecreation = float(tempList[5])
                startingFlag = 1
            else:
                tempList = finalList[1]
                if maxCapacity < float(tempList[1]):
                    maxCapacity = float(tempList[1])
                if maxStability < float(tempList[13]):
                    maxStability = float(tempList[13])
                if maxFoody < float(tempList[2]):
                    maxFoody = float(tempList[2])
                if maxDrinking < float(tempList[4]):
                    maxDrinking = float(tempList[4])
                if maxRecreation < float(tempList[5]):
                    maxRecreation = float(tempList[5])
                fileWriter(outputFile, -1, finalList[1])
            print('---------------------------')
    outputFile.close()
    # writing the final max values to file
    completeName = os.path.join(filePath, 'maxStorage.csv')
    outputFile = open(completeName, 'w+')
    maxValuesWriter(outputFile, maxCapacity, maxStability, maxFoody, maxDrinking, maxRecreation)
    outputFile.close()
    return 1

def main():
    filePath=input('Enter directory path where you want output to be generated: ')
    directoryPath=input('Enter path of directory where data-set resides')
    #filePath="D:\\intuit_challange\\rit-challenge\\transaction-data\\inferenceData"
    val=start(filePath,directoryPath)
    if val!=-1:
        print('Opened resources have been closed.....')
        print('EXECUTION COMPLETED')
    elif val==-1:
        print('EXECUTION ABORTED')

if __name__=="__main__":
    main()