import numpy as np
import pandas as pd
import math


def iseven(number):
    return number % 2 == 0
def isodd(number):
    return number % 2 != 0

def test123(mean,variance,state,change=1):
    if state == 'normal':
        tupleadd = tuple((np.random.normal()*variance[i]*change+mean[i]) for i in range(len(mean)))
    elif state == 'uniform':
        tupleadd = tuple(((np.random.rand()-0.5)*variance[i]*change+mean[i]) for i in range(len(mean)))
    return tupleadd
 
 #This essentially just creates a list of the upper function so that the top one is repeated over and over again.
def makebigarray(n,mean,variance,state,change=1):
    lista =[]
    for i in range(n):
        lista.append(test123(mean,variance,state,change))
    return lista

def findideal(testformula,bruteforcenp,storagearray):
    x, y = bruteforcenp.shape    
    arraysize = y-1
    combinationsize = (2**(arraysize))
    combolist = []
    
    #The first part is to generate all the possible directions that could arise from a point. In a 2D space, it would be 4 options, (Up and left), (up, right), (down, left), (down, right). However, this is expanded into
    # N generational space in the system of potental directions is 2^variable amount 

    for i in range(combinationsize):
        constring = ''
        for j in range(arraysize):
            if isodd(math.ceil((i+1)/(2**j))):
                constring = constring + 'D'
            elif iseven(math.ceil((i+1)/(2**j))): #Even
                constring = constring + 'U'
        combolist.append(constring)

    #Make a copy of the array because it keeps getting modified
    arraytest = bruteforcenp.copy()
    
    #Essentially just splits the whole thing
    for item in combolist:
        arraytest = bruteforcenp.copy()
        for i,j in enumerate(testformula):
            if item[i] == "U":
                arraytest = np.delete(arraytest,np.where((arraytest[:,i]<=j)),axis=0)
            elif item[i] == "D":
                arraytest= np.delete(arraytest,np.where((arraytest[:,i]>j)),axis=0)
        
        #Return the sum of the objective function in the split, the direction of the splits and the point which was tested
        storagearray.append([np.sum(arraytest[:,-1]),item,testformula])

    return storagearray

def returnarray(testformula,bruteforce,combolist):
    arraytest = bruteforce.copy()
    for i,j in enumerate(testformula):
        #print(combolist[i])
        if combolist[i] == "U":
            arraytest = arraytest[arraytest.iloc[:,i] > j]
            #print(arraytest)
        elif combolist[i] == "D":
            arraytest= arraytest[arraytest.iloc[:,i] <= j]
            #print(arraytest)
    return arraytest

class KnockoutPunch:
    def __init__(self,selected,remainder,ruleset):
        self.selected = selected
        self.remainder = remainder
        self.ruleset = ruleset

def FilterOutput(OutputArray,OriginalArray):
    #npgeneticdf = OriginalArray.to_numpy()
    listuse = list(OutputArray[np.argmax(OutputArray[:,0]),2])
    sequenceuse = list(OutputArray[np.argmax(OutputArray[:,0]),1])
    solutiontoproblem = returnarray(listuse,OriginalArray,sequenceuse)
    restofthesample = OriginalArray[~(OriginalArray.index.isin(solutiontoproblem.index))]
    ruleset = pd.DataFrame({'Variables':OriginalArray.columns[0:(len(OriginalArray.columns)-1)],'Directionality':sequenceuse,'Cutoffs':listuse})
    ruleset['Directionality']=ruleset['Directionality'].replace('U','>')
    ruleset['Directionality']=ruleset['Directionality'].replace('D','<=')

    return KnockoutPunch(solutiontoproblem,restofthesample,ruleset)

    #return solutiontoproblem, restofthesample, ruleset

#Same function, but it's generally all functioned up and therefore easier to call
def generatesplit(dataframe,batchsize,epochs,expdecayfac=0.99):
    npgeneticdf = dataframe.to_numpy()
    #change the output variable
    meanarray = np.mean(npgeneticdf[:,0:(len(dataframe.columns)-1)],axis=0)
    variancearray = np.std(npgeneticdf[:,0:(len(dataframe.columns)-1)],axis=0)
    storagearray = []
    storebest = []
    for l in range(epochs):
        if l == 0:
            #randomarraystores = []
            for i in range(batchsize):
                randomarraystores=makebigarray(batchsize,meanarray,variancearray*3,state="uniform")
                #randomarraystores.append((((np.random.rand()-0.5) * 20),(np.random.rand()-0.5) * 20,(np.random.rand()-0.5) * 20))
            for i in range(len(randomarraystores)):
                storagearray = findideal(randomarraystores[i],npgeneticdf,storagearray)
            npstoragearray = np.array(storagearray,dtype=object)
            newarray2 = list(npstoragearray[np.argmax(npstoragearray[:,0]),2])
            #bestiterationval = npstoragearray[np.argmax(npstoragearray[:,0]),0]
        if l > 0:
            #print(newarray2)
            if iseven(l):
                keephere = makebigarray(batchsize,newarray2,variancearray,state="normal",change=3.5)
                #keephere = newrandomness(newarray2,variancearray,batchsize,3)
            else:
                keephere = makebigarray(batchsize,newarray2,variancearray,state="normal",change = (0.3*(expdecayfac**l)))
                #keephere = newrandomness(newarray2,variancearray,batchsize,change = (0.3*(0.99**l)))
            storagearray = []
            for i in range(len(keephere)):
                storagearray = findideal(keephere[i],npgeneticdf,storagearray)
            npstoragearray = np.array(storagearray,dtype=object)
            bestiterationval = npstoragearray[np.argmax(npstoragearray[:,0]),0]
            if bestiterationval < npstorebest[np.argmax(npstorebest[:,0]),0]:
                newarray2 = list(npstorebest[np.argmax(npstorebest[:,0]),2])
            else:
                newarray2 = list(npstoragearray[np.argmax(npstoragearray[:,0]),2])
        storebest.append(npstoragearray[np.argmax(npstoragearray[:,0]),:])
        npstorebest = np.array(storebest,dtype=object)
        
    return (FilterOutput(npstorebest,dataframe))

