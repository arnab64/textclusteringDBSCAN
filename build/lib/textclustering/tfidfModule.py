from imp import reload
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib as mpl
import nltk,re,pprint
import sys,glob,os
import operator, string, argparse, math

# class to read and preprocess data
class dataProcessor:
    def __init__(self, fname, keep_factors = ['Job Description', 'Company Name', 'Industry'], group_column = 'Industry'):
        self.dataInitial = pd.read_csv(fname, encoding="latin")
        self.dataInitialSmall = self.dataInitial[['Job Description', 'Company Name', 'Industry']]
        self.swords = set(stopwords.words('english'))
        #print(len(self.swords),"stopwords present!")
        self.dataInitialGrouped = self.dataInitialSmall.groupby([group_column]).count()
        pd.set_option('display.max_rows', 50)
        print(self.dataInitialGrouped.sort_values(by=['Job Description'], ascending=False))

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

# primary tf-idf class
class flingTFIDF:
    def __init__(self,data,cname):
        self.idfMatrix = {}
        self.distanceMatrix = {}
        self.termsforIDF = []
        self.cname = cname
        self.data = data
        self.lenv = len(self.data)
        self.swords = set(stopwords.words('english'))

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

    def rem_stop_punct(self,originalText):
        splittedText = originalText.split()
        lenl = len(splittedText)
        wordFiltered = []
        tSent = []
        for r in range(lenl):
            wordx_1 = splittedText[r]
            wordx_2 = "".join(c for c in wordx_1 if c not in ('!','.',':',',','?',';','``','&','-','"','(',')','[',']','0','1','2','3','4','5','6','7','8','9')) 
            sWord = wordx_2.lower()
            if sWord not in self.swords:
                tSent.append(sWord)
        return " ".join(tSent)
        
    def smartTokenizeColumn(self):
        self.stopsRemoved = []
        for index, row in self.data.iterrows():
            prog=(index+1)/self.lenv
            originText = row[self.cname]
            sentx = self.rem_stop_punct(originText)
            self.drawProgressBar(prog)
            self.data.loc[index,'stopsRemoved'] = sentx
        self.cname = 'stopsRemoved'
        
    def getTF(self):
        print("\nAdding term frequency column based on",self.cname)
        tfMatrixList = []
        for index, row in self.data.iterrows():
            words_in_column = row[self.cname].split()
            if len(words_in_column)!=0:
                counts_all = Counter(words_in_column)
                words, count_values = zip(*counts_all.items())
                values_sorted, words_sorted = zip(*sorted(zip(count_values, words), key=operator.itemgetter(0), reverse=True))
                tfMatrixList.append(pd.DataFrame({'word': words_sorted, 'tf': values_sorted}))
                #self.data.loc[index,'tfMatrix'] = countdf
            else:
                #self.data.loc[index,'tfMatrix'] = pd.DataFrame(columns = ['word','tf'])
                tfMatrixList.append(pd.DataFrame(columns = ['word','tf']))
            prog=(index+1)/self.lenv
            self.drawProgressBar(prog)
        self.data['tfMatrix'] = tfMatrixList
        
    def getTFIDF(self):
        print("\nComputing and adding TF-IDF column based on",self.cname)
        for index, row in self.data.iterrows():
            tfmatrixThisrow = row['tfMatrix']
            tempTFIDF = []
            for indx, rwx in tfmatrixThisrow.iterrows():
                trmx = rwx['word']
                tfx = rwx['tf']
                idfx = self.idfMatrix[trmx]
                tfidfx = tfx*idfx
                tempTFIDF.append(tfidfx)
                #tfmatrixThisrow.loc[index,'tf-idf'] = tfidfx
            tfmatrixThisrow['tf-idf'] = tempTFIDF
            #sumtfidf = tfmatrixThisrow['tf-idf'].sum() 
            prog=(index+1)/self.lenv
            self.drawProgressBar(prog)
                
    def computeIDFlistofterms(self):
        totalwords = 0
        print("\nComputing list of words for IDF...\n")
        for index, row in self.data.iterrows():
            words_in_column = set(row[self.cname].split())  
            for word in words_in_column:
                if word not in self.termsforIDF:
                    self.termsforIDF.append(word)
                    totalwords+=1
        print("Created list of terms for IDF matrix with", totalwords," terms.")     
        
    def getIdf(self,term):
        countPresentDocs = 0
        lenidf = len(self.termsforIDF)
        for i in range(lenidf):
            tfx = self.getTermFreq(i,term)
            if tfx>0:
                countPresentDocs+=1
            prog=(i+1)/lenidf
            self.drawProgressBar(prog)
        return countPresentDocs
        
    def computeIDFmatrix(self):
        self.computeIDFlistofterms()
        print("\nComputing global IDF matrix...\n")
        for term in self.termsforIDF:
            self.idfMatrix[term]=0
        for index, row in self.data.iterrows():
            listofterms = list(self.data['tfMatrix'][index]['word'])
            for term in listofterms:
                self.idfMatrix[term]=self.idfMatrix[term]+1
            prog=(index+1)/self.lenv
            self.drawProgressBar(prog)
        for term in self.termsforIDF:
            idfx = self.idfMatrix[term]          
            idfy = self.lenv/float(1+idfx)
            idfz = math.log(idfy,10)
            self.idfMatrix[term] = idfz
            
    def showData(self):
        print(self.data['tfMatrix'])
        
    def createDistanceMetadata(self):
        #sumList = []
        for index, row in self.data.iterrows():
            tfmatrixThisrow = row['tfMatrix']
            sumTFIDF = tfmatrixThisrow['tf-idf'].sum()
            #sumList.append({'sumTFIDF':sumTFIDF})
            self.data.loc[index,'sumTFIDF'] = sumTFIDF
            prog=(index+1)/self.lenv
            self.drawProgressBar(prog)
              
    def distanceBtnTwoDocs(self, docId_1, docId_2):
        listWords_1 = set(list(self.data['tfMatrix'][docId_1]['word']))
        listWords_2 = set(list(self.data['tfMatrix'][docId_2]['word']))
        common = listWords_1.intersection(listWords_2)
        diff1_2 = listWords_1.difference(listWords_2)
        diff2_1 = listWords_2.difference(listWords_1)
        sumwt1 = self.data['sumTFIDF'][docId_1]
        sumwt2 = self.data['sumTFIDF'][docId_2]
        score_common, score_doc1, score_doc2 = 0,0,0
        for word_c in common:
            score_1 = float(self.data['tfMatrix'][docId_1].loc[self.data['tfMatrix'][docId_1]['word'] == word_c]['tf-idf'])
            score_2 = float(self.data['tfMatrix'][docId_2].loc[self.data['tfMatrix'][docId_2]['word'] == word_c]['tf-idf'])
            score_common += abs(score_1/float(sumwt1) - score_2/float(sumwt2))
        for word_d12 in diff1_2:
            score_1 = float(self.data['tfMatrix'][docId_1].loc[self.data['tfMatrix'][docId_1]['word'] == word_d12]['tf-idf'])
            score_doc1 += score_1/float(sumwt1)
        for word_d21 in diff2_1:
            score_2 = float(self.data['tfMatrix'][docId_2].loc[self.data['tfMatrix'][docId_2]['word'] == word_d21]['tf-idf'])
            score_doc2 += score_2/float(sumwt2)
        score_total = score_common + score_doc1 + score_doc2
        return(score_total)
    
    def computeDistanceBtnAllDocs(self):
        for j in range(100):
            for k in range(10):
                numx = j*10+k
                dist = self.distanceBtnTwoDocs(j,k)
                self.distanceMatrix[(j,k)] = dist
                prog=(numx+1)/1000
                self.drawProgressBar(prog)
                
        print(self.distanceMatrix[:10])
    
    def writeToFile(self,fname):
        self.data.to_csv(fname)