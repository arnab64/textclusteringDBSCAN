# exaluating the best cluster result. 

import time
cluster_file = __import__('4_cluster')
comparison_file = __import__('5_result_evaluation')
correct = [[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20],[21,22,23,24,25,26,27,28,29,30],[31,32,33,34,35,36,37,38,39,40],[41,42,43,44,45,46,47,48,49,50],[51,52,53,54,55,56,57,58,59,60]]				#write the correct cluster pattern here.

infile1 = open('scores.txt','r')
inlines = infile1.readlines()
lenx = len(inlines)
nof = 60 				#input the number of files here

def findscore(fid1,fid2):
	fidx1 = str(fid1)
	fidx2 = str(fid2)
	for k in range(lenx):
		linex = inlines[k].split()
		fx1 = linex[0]
		fx2 = linex[1]
		scx = linex[2]
		if fidx1==fx1 and fidx2==fx2:
			return float(scx)
			break;

def find_near_threshold():
	num = 0
	scorex = 0
	for k in range(nof):
		for j in range(k+1,nof):
			scr = findscore(k+1,j+1)
			num = num + 1
			scorex = scorex + scr
	print scorex, num
	nt = scorex/num
	#print "threshold = ", nt
	return nt
	
init_threshold = find_near_threshold()	
print init_threshold
threx = round(init_threshold, 2)

ofiley = open('results_threshold.txt','w')

threshold = threx - 0.2 
maxx = 0
best_threshold = 0
for h in range(40):
	threshold = threshold + 0.01
	arrx = cluster_file.main_prog(nof,threshold)
	scorexx = comparison_file.find_all(nof,arrx,correct)
	if scorexx > maxx:
		maxx = scorexx
		best_threshold = threshold
	print threshold, " / ", scorexx
	ofiley.write(str(threshold))
	ofiley.write("	")
	ofiley.write(str(scorexx))
	ofiley.write("\n")
	
print "maxx is ", maxx,"with threshold" , best_threshold

arrx = cluster_file.main_prog(nof,best_threshold)
print "arrx = ", arrx

