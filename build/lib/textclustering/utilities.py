def getallfilenames(foldername):#returns the name of all files inside the source folder. 		
    owd = os.getcwd()
    fld = foldername + "/"
    os.chdir(fld)					#this is the name of the folder from which the file names are returned.
    fnamearr = []						#empty array, the names of files are appended to this array, and returned.
    for file in glob.glob("*.txt"):
        fnamearr.append(file)
    os.chdir(owd)
    return fnamearr

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
    
def rem_stop_punct(originalText):
    splittedText = originalText.split()
    lenl = len(splittedText)
    wordFiltered = []
    tSent = []
    for r in range(lenl):
        wordx_1 = splittedText[r]
        wordx_2 = "".join(c for c in wordx_1 if c not in ('!','.',':',',','?',';','``','&','-','"','(',')','[',']','0','1','2','3','4','5','6','7','8','9')) 
        sWord = wordx_2.lower()
        if sWord not in swords:
            tSent.append(sWord)
    return " ".join(tSent)

def testUtilities():
    return ('ping! its all good!')