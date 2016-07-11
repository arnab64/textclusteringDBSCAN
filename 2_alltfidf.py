import math
import glob, os

'''def allfiles():						#returns the name of all files inside the source folder. 		
	owd = os.getcwd()
	os.chdir("sour/")				#this is the name of the folder from which the file names are returned.
	arr = []						#empty array, the names of files are appended to this array, and returned.
	for file in glob.glob("*.txt"):
		arr.append(file)
	os.chdir(owd)
	return arr '''

def allfiles(foldername):			#returns the name of all files inside the source folder. 		
	owd = os.getcwd()
	fld = foldername + "/"
	os.chdir(fld)					#this is the name of the folder from which the file names are returned.
	arr = []						#empty array, the names of files are appended to this array, and returned.
	for file in glob.glob("*.txt"):
		arr.append(file)
	os.chdir(owd)
	return arr

def extract_text(filex):			#returns the text inside a file, unedited. 
	f1 = open(filex,'r')			# input is the filename, and returned is all the text as a string.
	ftext = f1.read()
	f1.close()
	return ftext
	
def find_count(texts,word):			#finds the number of occurrence of a word in a text
	lenj = len(texts)
	fre1 = 0
	for j in range(lenj):
		if texts[j]==word:
			fre1 = fre1 + 1
	return fre1
	
def find_tf(text1,word):			# finds the term frequency of a word in a text, uses the 'find_count' method
	lenj = len(text1)
	fre1 = 0
	for j in range(lenj):
		if text1[j]==word:
			fre1 = fre1 + 1
	tf = math.log(1+fre1)			#check out the other methods of finding TF, from Wikipedia. I used the logarithmic method.
	return tf	
	
def find_idf(infile,word):
	arrk = allfiles('stops_removed')
	lenarrk = len(arrk)
	wc = 0
	for i in range(lenarrk):
		fname = "stops_removed/" + arrk[i]
		words1 = extract_text(fname)
		words2 = words1.split()
		if word in words2:			# if the given word is present in the file checked, increase count 
			wc = wc + 1
	fact = lenarrk/float(1+wc)
	logg1 = math.log(fact,10)
	return logg1
	
def find_tfidf(infile,text1,word):		# finds tf, finds idf, multiplies the two and returns tfidf.
	tf1 = find_tf(text1,word)		
	idf1 = find_idf(infile,word)
	tfidf1 = tf1*idf1				
	return tfidf1

def cluster_to_characteristic(infile,outfile):		# this function prints the tfidf scores of all words in a file.
	outx = open(outfile,'w')							# fxx = the output file i.e. the characteristic file
	texta = extract_text(infile)						# infile
	textw = texta.split()
	lent = len(textw)
	textu = []								#textu list contains all the unique words.
	for i in range(lent):
		if textw[i] not in textu:
			textu.append(textw[i])
	lentu = len(textu)
	for i2 in range(lentu):
		yy = find_tfidf(infile,textw,textu[i2])					# send the text list itself
		#print "---->", textu[i2], yy
		tff1 = find_count(textw,textu[i2])
		outx.write(textu[i2])
		outx.write("	")
		outx.write(str(yy))
		outx.write("\n")
	
def allconvert():	
	array1 = allfiles('stops_removed')
	lenv = len(array1)
	for k in range(lenv):
		in1 = 'stops_removed/'+array1[k];
		out1 = 'dest/'+array1[k];
		cluster_to_characteristic(in1,out1)

def main():
	allconvert()
	
if __name__ == '__main__':
	main()