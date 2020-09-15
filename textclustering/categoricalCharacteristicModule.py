# generate and save characteristic file from text column of csv file and a categorical variable

from imp import reload
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib as mpl
import nltk,re,pprint
import sys,glob,os
import operator, string, argparse, math

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

class flingCategoricalTFIDF:
    def __init__(self):
        self.nom = 0
        self.allfiles = []
        self.tfidfMatrix = []
        self.tfmatrixAllfiles = []
        self.termsforIDF = []
        self.idfMatrix = {}
        self.termsforIDF = []
        self.computed_tfmatrix = 0
        self.computed_idfmatrix = 0
        self.computed_IDFlistofterms = 0
        
    def drawProgressBar(self,percent, barLen = 50):			#just a progress bar so that you dont lose patience
        sys.stdout.write("\r")
        progress = ""
        for i in range(barLen):
            if i<int(barLen * percent):
                progress += "="
            else:
                progress += " "
        sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
        sys.stdout.flush()
        
    def getallfilenames(self,foldername):
        owd = os.getcwd()
        fld = foldername + "/"
        os.chdir(fld)
        fnamearr = []
        for file in glob.glob("*.txt"):
            fnamearr.append(file)
        os.chdir(owd)
        return fnamearr        
        
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
        if self.computed_tfmatrix==0:
            owd = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN"
            print(owd)
            fld = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles/"
            os.chdir(fld)

            for file in glob.glob("*.txt"):
                self.allfiles.append("/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles/" + file)   #this factor self.allfiles is not used, but just to record filename
                doctf = self.getDocumentTF(file)
                self.tfmatrixAllfiles.append(doctf)
            os.chdir(owd)
            self.computed_tfmatrix=1
        else:
            print("tf matrix already computed")
        self.nom = len(self.tfmatrixAllfiles)
        
    def getTermFreq(self,docId,term):
        valx = self.tfmatrixAllfiles[docId][self.tfmatrixAllfiles[docId]['word']==term]['count'].tolist()
        if len(valx)==0:
            return 0
        return valx[0]
        
    def computeIDFlistofterms(self):
        totalwords = 0
        for file in self.allfiles:
            print("IDF processing...",file)    
            file1 = open(file)
            readfile = file1.read()
            wordsInFile = readfile.split()
            lenx=len(wordsInFile)
            totalwords+=lenx
            self.termsforIDF.extend(set(wordsInFile))
        print("Created list of terms for IDF matrix with", len(self.termsforIDF)," terms i.e. ",len(self.termsforIDF)/totalwords*100," of total words!")
        self.computed_IDFlistofterms = 1
        
    def getIdf(self,term):
        countPresentDocs = 0
        for i in range(self.nom):
            tfx = self.getTermFreq(i,term)
            if tfx>0:
                countPresentDocs+=1
        return countPresentDocs

    def computeIDFmatrix(self):
        if self.computed_IDFlistofterms == 0:
            self.computeIDFlistofterms()
        lenv = len(self.termsforIDF)
        if self.computed_idfmatrix==0:        
            print("Computing inverse document frequencies for ",lenv,"terms!")
            for j in range(lenv):
                el = self.termsforIDF[j]
                idfx = self.getIdf(el)
                idfy = lenv/float(1+idfx)
                idfz = math.log(idfy,10)
                self.idfMatrix[el] = [idfz]
                prog=(j+1)/lenv
                self.drawProgressBar(prog)
            self.computed_idfmatrix=1
        else:
             print("IDF matrix already computed, with", len(self.termsforIDF),"terms!")
        
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
        
    def generateCategoricalCharacteristicFiles(self):
        print(len(ft.tfidfMatrix),"matrix files available!")
        for matrixID in range(len(ft.tfidfMatrix)):
            fname_orig = allfnames[matrixID]
            newfname = fname_orig.split()[0]+'_characteristic.csv'
            print("filename:",newfname)
            matrixDF = pd.DataFrame.from_dict(ft.tfidfMatrix[matrixID], orient = 'index')
            matrixDF.to_csv(newfname, header=False)
            
    def computeTFIDFallfiles(self,flist):
        lenflist = len(flist)
        if self.computed_tfmatrix == 0:
            self.computeTFmatrix()
        if self.computed_idfmatrix == 0:
            self.computeIDFmatrix()        
        for fin in range(lenflist):
            fname = "/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles/" + flist[fin]
            print("file:",fname)
            tfidfMAT = self.compute_tfidf(fin,fname)
            self.tfidfMatrix.append(tfidfMAT)
            prog=(fin+1)/lenflist
            self.drawProgressBar(prog)           
        print("tfidfMatrix created for ",len(self.tfidfMatrix),"documents!")
        self.generateCategoricalCharacteristicFiles()