import matplotlib.pyplot as plt

infile1 = open('txt1.txt','r')
inlines = infile1.readlines()
lenx = len(inlines)

arr1 = []
arr2 = []
arr3 = []
arr4 = []

for k in range(lenx):
	linex = inlines[k].split()
	print linex
	arr1.append(float(linex[0]))
	arr2.append(float(linex[1]))
	arr3.append(float(linex[2]))
	arr4.append(float(linex[3]))
'''	
plt.plot(arr1,arr4)
plt.show()'''