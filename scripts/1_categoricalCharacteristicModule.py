import fasttext
import pandas as pd
import numpy as np
import matplotlib as mpl
import nltk,re,pprint
import sys,glob,os
from imp import reload
from nltk.corpus import stopwords
from collections import Counter
import operator
import string
import argparse

'''dataAnalyst = pd.read_csv("../datasets/DataAnalyst.csv", encoding="latin")
#dataAnalystSmall = dataAnalyst[['Job Description', 'Company Name', 'Industry']]

dataAnalystGrouped = dataAnalystSmall.groupby(['Industry']).count()
pd.set_option('display.max_rows', 500)
print(dataAnalystGrouped.sort_values(by=['Job Description'], ascending=False))

dataAnalystTopCat = dataAnalystSmall[dataAnalystSmall["Industry"].isin(['IT Services', 'Staffing & Outsourcing', 'Health Care Services & Hospitals', 'Consulting',
'Computer Hardware & Software', 'Investment Banking & Asset Management', 'Enterprise Software & Network Solutions', 'Internet',
'Banks & Credit Unions', 'Advertising & Marketing'])]'''

def drawProgressBar(percent, barLen = 50):			#just a progress bar so that you dont lose patience
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i<int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()

class dataProcessor:
    def __init__(self, fname, keep_factors = ['Job Description', 'Company Name', 'Industry'], group_column = 'Industry'):
        self.dataInitial = pd.read_csv(fname, encoding="latin")
        self.dataInitialSmall = self.dataInitial[['Job Description', 'Company Name', 'Industry']]
        self.swords = set(stopwords.words('english'))
        #print(len(self.swords),"stopwords present!")
        self.dataInitialGrouped = self.dataInitialSmall.groupby([group_column]).count()
        pd.set_option('display.max_rows', 50)
        print(self.dataInitialGrouped.sort_values(by=['Job Description'], ascending=False))
        
    def customProcessData(self):
        self.dataTopCat = self.dataInitialSmall[self.dataInitialSmall["Industry"].isin(['IT Services', 'Staffing & Outsourcing', 'Health Care Services & Hospitals', 'Consulting',
'Computer Hardware & Software', 'Investment Banking & Asset Management', 'Enterprise Software & Network Solutions', 'Internet',
'Banks & Credit Unions', 'Advertising & Marketing'])]
        self.dataTopCatGrouped = self.dataTopCat.groupby(['Industry'])['Job Description'].apply(lambda x: ','.join(x)).reset_index()
        self.dataTopCatGrouped.reset_index()

    # pipeline for purifying the text, write-pipeline, so just output filename can be provided
    def rem_stop_punct(self,originalText, ofilename):
        splittedText = originalText.split()
        lenl = len(splittedText)
        print("Length is: ",lenl, splittedText[:5])
        ofile = open(ofilename,'a')
        
        for r in range(lenl):
            linex = splittedText[r]
            linex2 = "".join(c for c in linex if c not in ('!','.',':',',','?',';','``','&','-','"','(',')','[',']','0','1','2','3','4','5','6','7','8','9'))
            linex3 = linex2.split()
            #prog=(r+1)/len(rawlines)
            for s in range(len(linex3)):
                noword = linex3[s].lower()
                if noword not in self.swords:
                    ofile.write(noword)
                    ofile.write(" ") 

# using the class dataProcessor                    
rp = dataProcessor("../datasets/DataAnalyst.csv")
rp.customProcessData()
for index, row in rp.dataTopCatGrouped.iterrows():
    ofname = '../processFiles/trainCatFiles/cat' + str(index)+ '_' + ''.join(row['Industry'].split()) + '.txt'    
    print("Processing...",ofname)
    rp.rem_stop_punct(row['Job Description'],ofname)
    

# ------------------------------------------ starting TF-IDF     


def getTermFreq(docId,term):
    valx = arrTermFreq[docId][arrTermFreq[docId]['word']==term]['count'].tolist()
    if len(valx)==0:
        return 0
    return valx[0]
    




    
#Inverse Document Frequency(IDF)

import math

owd = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN"
print(owd)
fld = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles/"
os.chdir(fld)
termsForIDF = []
totalwords = 0 
for file in glob.glob("*.txt"):
    print("found",file)    
    file1 = open(file)
    readfile = file1.read()
    wordsInFile = readfile.split()
    lenx=len(wordsInFile)
    totalwords+=lenx
    termsForIDF.extend(set(wordsInFile))
print(len(termsForIDF),totalwords)

def getIdf(term):
    countPresentDocs = 0
    for i in range(len(arrTermFreq)):
        tfx = getTermFreq(i,term)
        #print(tfx)
        if tfx>0:
            countPresentDocs+=1
            #print("found one")
    #print(countPresentDocs,"countPresentDocs")
    return countPresentDocs
    
    return logg1

#idfMatrix = {'term':'Zara','idfx':'1'}
idfMatrix = {}
lenv = len(termsForIDF)
#lenv = 100
print("Computing inverse document frequencies")
for j in range(lenv):
    el = termsForIDF[j]
    idfx = getIdf(el)
    idfy = lenv/float(1+idfx)
    idfz = math.log(idfy,10)
    idfMatrix[el] = [idfz]
    prog=(j+1)/lenv
    drawProgressBar(prog)
    
#pd.DataFrame(idfMatrix)
idfMatrixDF = pd.DataFrame.from_dict(idfMatrix, orient = 'index')


owd = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN"
os.chdir(owd)
idfMatrixDF.to_csv('processFiles/idfMatrixDF.csv', header=False)

#tfidf

class flingCategoricalTFIDF:
    def __init__(self):
        self.nof = 0
        self.allfiles = []
        self.tfidfMatrix = []
        self.tfmatrixAllfiles = []
        self.termsforIDF = []
        #allfnames = self.allfiles("/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles")

    def getDocumentTF(self,fname):
        file1 = open(fname)
        readfile = file1.read()
        wordsInFile = readfile.split()
        counts_all = Counter(wordsInFile)
        words, count_values = zip(*counts_all.items())
        values_sorted, words_sorted = zip(*sorted(zip(count_values, words), key=operator.itemgetter(0), reverse=True))
        countdf = pd.DataFrame({'count': values_sorted, 'word': words_sorted})
        return countdf

    def computeTFmatrix(self):
        owd = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN"
        print(owd)
        fld = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles/"
        os.chdir(fld)
        
        for file in glob.glob("*.txt"):
            self.allfiles.append("/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles/" + file)   #this factor self.allfiles is not used, but just to record filename
            doctf = getDocumentTF(file)
            self.tfmatrixAllfiles.append(doctf)
        os.chdir(owd)
        print(len(self.tfmatrixAllfiles))
        
    def computeIDFbasic(self):
        totalwords = 0
        for file in self.allfiles:
            print("IDF processing...",file)    
            file1 = open(file)
            readfile = file1.read()
            wordsInFile = readfile.split()
            lenx=len(wordsInFile)
            totalwords+=lenx
            self.termsforIDF.extend(set(wordsInFile))
        print(len(self.termsforIDF),totalwords)

    def getIdf(term):
        countPresentDocs = 0
        for i in range(len(arrTermFreq)):
            tfx = getTermFreq(i,term)
            #print(tfx)
            if tfx>0:
                countPresentDocs+=1
                #print("found one")
        #print(countPresentDocs,"countPresentDocs")
        return countPresentDocs
        
    def compute_tfidf(self,fileIndex,filename):
        tfidfFileMatrix = {}
        file1 = open(filename)
        readfile = file1.read()
        wordsInFile = set(readfile.split())
        for word in wordsInFile:
            tf_final = getTermFreq(fileIndex,word)
            idf_final = idfMatrix[word][0]
            tfidf_final = tf_final * idf_final
            tfidfFileMatrix[word] = tfidf_final
        return tfidfFileMatrix
        
    def getallfilenames(self,foldername):#returns the name of all files inside the source folder. 		
        owd = os.getcwd()
        fld = foldername + "/"
        os.chdir(fld)					#this is the name of the folder from which the file names are returned.
        fnamearr = []						#empty array, the names of files are appended to this array, and returned.
        for file in glob.glob("*.txt"):
            fnamearr.append(file)
        os.chdir(owd)
        return fnamearr
        
    def computeTFIDFallfiles(self,flist):
        for fin in range(len(flist)):
            fname = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles/" + flist[fin]
            print("file:",fname)
            tfidfMAT = self.compute_tfidf(fin,fname)
            self.tfidfMatrix.append(tfidfMAT)
        print("length of tfidfMatrix:",len(self.tfidfMatrix))        
        
    def generateCategoricalCharacteristicFiles(self):
        print(len(ft.tfidfMatrix))
        for matrixID in range(len(ft.tfidfMatrix)):
        fname_orig = allfnames[matrixID]
        newfname = fname_orig.split()[0]+'_characteristic.csv'
        print("filename:",newfname)
        matrixDF = pd.DataFrame.from_dict(ft.tfidfMatrix[matrixID], orient = 'index')
        matrixDF.to_csv(newfname, header=False)

# save characteristic files for categories assigned 
fwd = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/characteristicFiles"
os.chdir(fwd)
os.chdir("/Users/arnabborah/Documents/repositories/textclusteringDBSCAN")

ft = flingCategoricalTFIDF()
allfnames = ft.getallfilenames("/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles")
ft.computeTFIDFallfiles(allfnames)
print(len(ft.tfidfMatrix))
print(len(idfMatrix))



    