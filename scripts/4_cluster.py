import sys
#clustering using DBSCAN
#implementing DBSCAN from scratch

class dbscan:
	def __init__(self):
		print("DBSCAN initialized!\n")

	def findscore(self,fid1,fid2):
		infile1 = open('scores.txt','r')
		inlines = infile1.readlines()
		lenx = len(inlines)
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

	def find_near(self,fidx,noff,near_threshold):
		nearlist = []
		for k in range(noff):
			if fidx!=(k+1):
				scrz = self.findscore(fidx,k+1)
				if scrz<near_threshold:
					nearlist.append(k+1)
		return nearlist

	def find_diff(self,arr1,arr2):
		arr3 = []
		for el in arr1:
			if el not in arr2:
				arr3.append(el)
		return arr3
		
	def find_near_final(self,listx,noff,near_threshold):
		nearlist = []
		for elm in listx:
			gyyy = self.find_near(elm,noff,near_threshold)
			for rt in gyyy:
				if rt not in nearlist:
					nearlist.append(rt)
		#print "nearlist : ", nearlist
		return nearlist
		
	def find_find(self,listy,done,noff,near_threshold):
		nearx = self.find_near_final(listy,noff,near_threshold)
		done.extend(listy)
		diffx = self.find_diff(nearx,done)
		#print "diffx = ", diffx
		lendiffx = len(diffx)
		if lendiffx!=0:
			self.find_find(diffx,done,noff,near_threshold)
		return done	

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

	def main_prog(self,noff,near_threshold):
		ofile1 = open('clusters.txt','w')
		done = []
		finalx = []
		for y in range(noff):
			temparr = []
			if y+1 not in done:
				prev = []
				prev.extend(done)
				firstlist = []
				firstlist.append(y+1)
				done = self.find_find(firstlist,done,noff,near_threshold)
				diff = self.find_diff(done,prev)
				for ol in diff:
					temparr.append(ol)
					ofile1.write(str(ol))
					ofile1.write(" ")
				ofile1.write("\n")
				finalx.append(temparr)
		ofile1.close()
		return finalx
	
if __name__ == '__main__':
	dbs=dbscan()
	dbs.main_prog(60,1.80)