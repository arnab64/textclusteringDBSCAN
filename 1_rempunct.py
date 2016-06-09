#remove punctuations! basic text processing
# to do : remove the [num] found in wikipedia pages. 

import nltk,re,pprint
import sys,glob,os

reload(sys)
sys.setdefaultencoding('latin1')

from nltk.corpus import stopwords
sw = open('stopwords.txt','r').read()
swords = sw.split()
print len(swords)

def allfiles(foldername):			#returns the name of all files inside the source folder. 		
	owd = os.getcwd()
	fld = foldername + "/"
	os.chdir(fld)					#this is the name of the folder from which the file names are returned.
	arr = []						#empty array, the names of files are appended to this array, and returned.
	for file in glob.glob("*.txt"):
		arr.append(file)
	os.chdir(owd)
	return arr

def rem_stop(fname,ofilename):
	rawlines = open(fname).readlines()
	lenl = len(rawlines)
	of=open(ofilename,'w')
	for r in range(lenl):	
		linex = rawlines[r]
		linex2 = "".join(c for c in linex if c not in ('!','.',':',',','?',';','``','&','-','"','(',')','[',']','0','1','2','3','4','5','6','7','8','9'))
		linex3 = linex2.split()
		for s in range(len(linex3)):
			noword = linex3[s].lower()
			if noword not in swords:
				of.write(noword)
				of.write(" ")
		of.write("\n")

def allremove():	
	array1 = allfiles('source')						# give the name of the folder which files you want to import!!
	lenv = len(array1)
	for k in range(lenv):
		in1 = 'source/'+array1[k];
		out1 = 'stops_removed/'+array1[k];			# foldername of the output folder, create the folder first, if does not exist
		rem_stop(in1,out1)

allremove()
#rem_stop('walmart.txt','polished.txt')