__author__="Varun Rajiv Mantri"
import csv
import os

def csvReader(fileName):
    startingLineFlag = 0
    file = open(fileName)
    fileread = csv.reader(file)
    print(fileName)
    return [fileread,file]

def hashStringer(key):
    alternater = 1
    result = ''
    if len(key) != 1:
        for item in key:
            if alternater == 1:
                val = str((ord(item) - 22) * 9)
                result = result + val[len(val) - 2]
                alternater = -1
            else:
                val = str((ord(item) - 22) * 9)
                result = result + val[1]
                alternater = 1
    else:
        result = ord(key)
    result = str(result * 31)
    sum = 0
    for item in result:
        sum = sum + int(item)
    if sum % 2 == 0:
        result = int(result) >> 1
        result = str(result - 1)
    else:
        result = str(int(result) >> 2)
    return int(result)

'''
def totalIncome(fileName):
    listFile=csvReader(fileName)
    file=listFile[0]
    startingLineFlag = 0
    totalSpending=0
    totalPayment=0
    for row in file:
        if startingLineFlag == 0:
            startingLineFlag = 1
        else:
            tempVal=float(row[3])
            if tempVal<0:
                totalSpending=totalSpending+tempVal
            else :
                totalPayment=totalPayment+tempVal
    #closing the openned resource
    file=listFile[1]
    file.close()
    #-----------------------
    totalPayment=(totalPayment)/2
    temp=0.24*totalPayment
    totalIn=totalPayment+temp
    return (totalIn)
'''
def initializationCode():
    keyWordList = table = [None for _ in range(1000)]
    featureList = ['User ID','Financial Capacity', 'Food', 'Transportation', 'Drinking', 'Recreation', 'House?','parent?', 'student?', 'car?','pet?','Divorced?','Expenditure post paycheck','Financial stability']
    tempList = [['Public Transportation', 3], ['Restaurant', 2], ['Taxi', 3], ['Uber', 3], ['Bar', 4],['Foods',2],
                ['Night Club', 4], ['Inn', 5], ['Brewery', 4],['Wine',4], ['Housing Rent', 6], ['Pet',10],['Divorce',11],['Online Education Courses',8],['Student',8],['Babies',7],['Bowling',5],['Movie Ticket',5],['Concert',5],['Ice Skating Rink',5],['Museum',5]]
    plist=[]
    for item in tempList:
        index = hash(item[0]) % 1000
        collision=0
        '''while keyWordList[index] != None:
            index = index + 1'''
        if keyWordList[index]!=None:
            collision=collision+1
        plist.append(index)
        keyWordList[index] = item
    print(collision)
    return  [keyWordList,featureList]

def featureExtracter(fileName):
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


    '''
        if annual income is 0 then the person is jobless and the figures are computed by considering income to be 1
        thus the featureData is not altered
    '''
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


def inferenceBuilder(featureData,annualIncome):
    # converting to percentage and building inference
    referenceList = [2, 3, 4, 5, 10]
    if annualIncome != 0:
        for item in referenceList:
            temp = float(featureData[item])
            featureData[item] = ((temp / annualIncome) * 100)
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
    if featureList!=-1:
        for item in featureList:
            file.write(str(item)+',')
        file.write('\n')
    for item in featureData:
        file.write(str(item)+',')
    file.write('\n')

def maxValuesWriter(file,maxCapacity,maxStability,maxFoody,maxDrinking,maxRecreation):
    file.write('MaxCapacity,MaxStability,maxFoodyness,maxDrinking,maxRecreation\n')
    file.write(str(maxCapacity)+','+str(maxStability)+','+str(maxFoody)+','+str(maxDrinking)+','+str(maxRecreation)+'\n')

def helperExtracter(wordList,keyWordList):
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

'''
def inferenceEngine(fileName):
    fileRead=csvReader(fileName)
    fileHandle=fileRead[0]
    startingFlag=0
    modifiedFeatureData=[None for _ in range(14)]
    referenceList=[2,3,4,5,10]
    for row in fileHandle:
        if startingFlag==0:
            startingFlag=1
        else:
            print(row[1])
            baseIncome=float(row[1])
            for item in referenceList:
                temp=float(row[item])
                modifiedFeatureData[item]=((temp/baseIncome)*100)
    fileRead[1].close()
    return modifiedFeatureData
'''

def main():
    filePath="D:\\intuit_challange\\rit-challenge\\transaction-data\\inferenceData"
    completeName = os.path.join(filePath,'intermediateOutPut.csv')
    outputFile = open(completeName, 'w+')
    startingFlag=0
    # Storing the maximum values in file
    maxCapacity = 0
    maxStability=0
    maxFoody=0
    maxDrinking=0
    maxRecreation=0
    for file in os.listdir('D:\\intuit_challange\\rit-challenge\\transaction-data'):
        if file.endswith('.csv'):
            print(file)
            finalList=featureExtracter(file)
            if startingFlag==0:
                fileWriter(outputFile,finalList[0],finalList[1])
                tempList=finalList[1]
                maxCapacity=float(tempList[1])
                maxStability=float(tempList[13])
                maxFoody=float(tempList[2])
                maxDrinking=float(tempList[4])
                maxRecreation=float(tempList[5])
                startingFlag=1
            else:
                tempList = finalList[1]
                if maxCapacity <float(tempList[1]):
                    maxCapacity=float(tempList[1])
                if maxStability < float(tempList[13]):
                    maxStability=float(tempList[13])
                if maxFoody < float(tempList[2]):
                    maxFoody=float(tempList[2])
                if maxDrinking < float(tempList[4]):
                    maxDrinking=float(tempList[4])
                if maxRecreation < float(tempList[5]):
                    maxRecreation=float(tempList[5])
                fileWriter(outputFile,-1,finalList[1])
            print('---------------------------')
    outputFile.close()
    #writing the final max values to file
    completeName = os.path.join(filePath,'maxStorage.csv')
    outputFile = open(completeName, 'w+')
    maxValuesWriter(outputFile,maxCapacity,maxStability,maxFoody,maxDrinking,maxRecreation)
    outputFile.close()
    print('Opened resources have been closed.....')
main()