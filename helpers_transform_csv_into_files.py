
import sys
import re
import io
import six
print(sys.argv)


class transformCSV:
    def __init__(self):
        print("Transform module initialized!")

    def read_input(self):
        rawlines = io.open(sys.argv[1], mode="r", encoding="utf-8").readlines()

        # # first line is the header
        # linesize = len(re.split(r'\t+', rawlines[0]))
        # print("linesize", linesize)

        for i in range(1, len(rawlines)):
            line = rawlines[i]
            print(line)
            phrases = re.split(r'\t+', line)

            # I use the email as the name of the file
            email = ""
            for phrase in phrases:
                if (phrase and isinstance(phrase, six.string_types) and phrase.find("@") >= 0):
                    email = phrase.lower()

            print(email)

            of = open("source/" + email + ".txt", 'w')
            of.write(line.encode('UTF-8'))
            of.close()

    def main(self):
        self.read_input()
        # oscores = open('scores.txt','w')
        # filex = self.allfiles('dest')
        # lenn = len(filex)
        # total = lenn*lenn
        # for g in range(lenn):
        # 	file1 = 'dest/' + filex[g]
        # 	for h in range(lenn):
        # 		prog = (g*lenn+h)/total
        # 		file2 = 'dest/' + filex[h]
        # 		if file1!=file2:
        # 			scr = self.matchscore(file1,file2)
        # 			fx1 = self.find_fileid(file1)
        # 			fx2 = self.find_fileid(file2)
        # 			oscores.write(fx1)
        # 			oscores.write("	")
        # 			oscores.write(fx2)
        # 			oscores.write("	")
        # 			oscores.write(str(scr))
        # 			#print(fx1,fx2,scr)
        # 			oscores.write("\n")
        # 			self.drawProgressBar(prog)


if __name__ == '__main__':
    distx = transformCSV()
    distx.main()
