#this program finds the distance between two files. The distance is measured from the tfidf scores of two files.
#the function which finds the distance is matchscore(), the input parameters to the function is the names of the two files. 

import glob,os

def sum_weight(file):				#finds sum of all the scores in a tfidf file 
	f1 = open(file,'r')
	f2 = f1.readlines()
	lenf2 = len(f2)
	weight = 0.0
	likelihood = 0.0
	for t in range(lenf2):
		line1 = f2[t]
		line2 = line1.split()
		weight = weight + float(line2[1])
	return weight

def allfiles(foldername):			#returns the name of all files inside the source folder. 		
	owd = os.getcwd()
	fld = foldername + "/"
	os.chdir(fld)					#this is the name of the folder from which the file names are returned.
	arr = []						#empty array, the names of files are appended to this array, and returned.
	for file in glob.glob("*.txt"):
		arr.append(file)
	os.chdir(owd)
	return arr

def positive(n):
	if n < 0:
		return -n
	else:
		return n

def handle_one(tot1,p,sumweight):
	tot2 = tot1 + p/float(sumweight)
	return tot2

def handle_both(tot2,p,q,sumweight1,sumweight2):
	score = p/float(sumweight1) - q/float(sumweight2)
	points = positive(score)
	return tot2 + points

def find_fileid(str1):				# returns only the file id from the full filename/path
	str2 = str1[5:]
	lenstr = len(str2)
	if lenstr==5:
		return str2[0]
	elif lenstr==6:
		return str2[:2]
	else:
		return str2[:3]
	
def matchscore(str1,str2):
	file1 = open(str1,'r')
	flines1 = file1.readlines()
	len1 = len(flines1)

	file2 = open(str2,'r')	
	flines2 = file2.readlines()
	len2 = len(flines2)

	#print "len1 and len2 = ", len1, len2,"\n";

	words1 = []
	words2 = []
	scores1 = []
	scores2 = []
	
	for j in range(len1):
		linex1 = flines1[j].split()
		words1.append(linex1[0])
		scores1.append(float(linex1[1]))
	
	for k in range(len2):
		linex2 = flines2[k].split()
		words2.append(linex2[0])
		scores2.append(float(linex2[1]))

	common = []
	diff1 = []
	diff2 = []
	
	for g1 in range(len1):
		if words1[g1] in words2:
			common.append(words1[g1])
		else:
			diff1.append(words1[g1])
	for g2 in range(len2):
		if(words2[g2] not in words1):
			diff2.append(words2[g2])
	
	lenx = len(common)
	lenx1 = len(diff1)
	lenx2 = len(diff2)

	#print "there are ",lenx," common words", lenx1,"&",lenx2,"unique words!\n" 

	sumweight1 = sum_weight(str1)
	sumweight2 = sum_weight(str2)
	
	#print "sumwight12 = ", sumweight1,sumweight2

	totx = 0

	for gx1 in range(lenx):
		term1 = common[gx1]
		ind1 = words1.index(term1)
		ind2 = words2.index(term1)
		totx = handle_both(totx, scores1[ind1],scores2[ind2],sumweight1,sumweight2)
	
	for gx2 in range(lenx1):
		term2 = diff1[gx2]
		indx2 = words1.index(term2)
		totx = handle_one(totx,scores1[indx2],sumweight1)
	
	for gx3 in range(lenx2):
		term3 = diff2[gx3]		
		indx3 = words2.index(term3)
		totx = handle_one(totx,scores2[indx3],sumweight2)

	return totx

oscores = open('scores.txt','w')
filex = allfiles('dest')
lenn = len(filex)
for g in range(lenn):
	file1 = 'dest/' + filex[g]
	for h in range(lenn):
		file2 = 'dest/' + filex[h]
		if file1!=file2:
			scr = matchscore(file1,file2)
			fx1 = find_fileid(file1)
			fx2 = find_fileid(file2)
			oscores.write(fx1)
			oscores.write("	")
			oscores.write(fx2)
			oscores.write("	")
			oscores.write(str(scr))
			print fx1,fx2,scr
			oscores.write("\n")	

print "the distance between the two files is i.e. score =", scr
