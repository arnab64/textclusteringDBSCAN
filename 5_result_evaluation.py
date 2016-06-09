# cluster performance measurement using Adjusted Rand Index

def check_items_correct(p,q,arrax):
	len1 = len(arrax)
	for y in range(len1):
		linethis = arrax[y]
		if (p in linethis) and (q in linethis):
			return 1
	return 0
	
def check_items_computed(p,q,corrx):
	len2 = len(corrx)
	for y in range(len2):
		linethis = corrx[y]
		if (p in linethis) and (q in linethis):
			return 1
	return 0
	
def find_all(nof,arrax,corrx):
	same1 = []
	same2 = []
	diff1 = []
	diff2 = []

	for k in range(nof):
		for j in range(k+1,nof):
			stat = check_items_correct(k+1,j+1,arrax)
			strx = str(k+1)+str(j+1)
			if stat==1:
				same1.append(strx)
			else:
				diff1.append(strx)
	#print same1,diff1			
	
	for k in range(nof):
		for j in range(k+1,nof):
			stat = check_items_computed(k+1,j+1,corrx)
			strx = str(k+1)+str(j+1)
			if stat==1:
				same2.append(strx)
			else:
				diff2.append(strx)
	aa = 0
	bb = 0
	for element in same1:
		if element in same2:
			aa=aa+1
	for elem in diff1:
		if elem in diff2:
			bb=bb+1
	nc2 = nof*(nof-1)/2
	scorex = (aa+bb)/float(nc2)
	#print aa,bb,nc2,
	return scorex
