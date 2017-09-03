#remove punctuations! basic text processing
# to do : remove the [num] found in wikipedia pages. 

import nltk,re,pprint
import sys,glob,os
from imp import reload
from nltk.corpus import stopwords

reload(sys)
#sys.setdefaultencoding('latin1')

class rempunct:
	def __init__(self):
		from nltk.corpus import stopwords
		#sw = open('stopwords.txt','r').read()
		#self.swords = sw.split()
		self.swords = set(stopwords.words('english'))
		print(len(self.swords),"stopwords present!")

	def allfiles(self,foldername):			#returns the name of all files inside the source folder. 		
		owd = os.getcwd()
		fld = foldername + "/"
		os.chdir(fld)					#this is the name of the folder from which the file names are returned.
		arr = []						#empty array, the names of files are appended to this array, and returned.
		for file in glob.glob("*.txt"):
			arr.append(file)
		os.chdir(owd)
		print("All filenames extracted!")
		return arr

	def rem_stop(self,fname,ofilename):
		rawlines = open(fname).readlines()
		lenl = len(rawlines)
		of=open(ofilename,'w')
		for r in range(lenl):	
			linex = rawlines[r]
			linex2 = "".join(c for c in linex if c not in ('!','.',':',',','?',';','``','&','-','"','(',')','[',']','0','1','2','3','4','5','6','7','8','9'))
			linex3 = linex2.split()
			prog=(r+1)/len(rawlines)
			for s in range(len(linex3)):	
				noword = linex3[s].lower()
				if noword not in self.swords:
					of.write(noword)
					of.write(" ")
			#self.drawProgressBar(prog)
			of.write("\n")


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

	def allremove(self):	
		array1 = self.allfiles('source')						# give the name of the folder which files you want to import!!
		lenv = len(array1)
		for k in range(lenv):
			progr=(k+1)/lenv
			in1 = 'source/'+array1[k];
			out1 = 'stops_removed/'+array1[k];			# foldername of the output folder, create the folder first, if does not exist
			self.rem_stop(in1,out1)
			self.drawProgressBar(progr)
		print("\nAll files done!")
		
if __name__ == '__main__':
	rp = rempunct()
	rp.allremove()
