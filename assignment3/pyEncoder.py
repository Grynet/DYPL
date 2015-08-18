'''
pyEncoder.py is used to encode numbers provided in a file of numbers into words that are provided 
by a file that contains words. 

'''
import sys

DICT = {
	"6":6, "k":7, "v":6, "7":7, "l":8, "a":5, "w":2, 
	"8":8, "b":7, "m":5, "x":2, "9":9, "c":6, "y":3, 
	"n":1, "z":9, "o":8, "d":3, "0":0, "p":8, "e":0, 
	"1":1, "f":4, "q":1, "2":2, "g":9, "r":2, "3":3, 
	"h":9, "s":3, "4":4, "i":6, "t":4, "5":5, "u":7, 
	"j":1
}

words = [] #holds words that has been read in from file
results = [] #holds the matching encodings for numbers

#returns a list of every entry in the file in lower case.
def readFile(filePath):
	with open(filePath, 'r') as theFile:
		return [word.rstrip('\n').replace("-","").lower() for word in theFile]

def wordToNumber(word):
	return ''.join(str(DICT[e]) for e in list(word))

#saves a successful number to word encoding
def addMatch(encoding):	
	results.append("%s : %s" %(wordToNumber(encoding.replace(" ","")), encoding))

#builds number encodings
def buildEncoding(number, encoding):
	for word in words:			
		if len(word) <= len(number):
			wordAsNumber = wordToNumber(word)
			if number.startswith(wordAsNumber):
				newEncoding =  (encoding + word) if encoding == "" else (encoding + " %s" % (word))
				findMatch(number[len(word):], newEncoding)	

#adds or builds number to word encodings
def findMatch(number, encoding):		
	if number == "":
		addMatch(encoding)
	else:
		buildEncoding(number, encoding)

#main takes a word and number file and encodes each number into matching words from the wordFile 
def main(argv):
	try:
		global words
		numberFilePath = argv[0]
		wordFilePath = argv[1]
		numbers = readFile(numberFilePath)
		words = readFile(wordFilePath)

		for number in numbers:
			findMatch(number, "")	

		for result in results:
			print result
	except:
		print "To execute: python pyEncoder.py <fileWithNumbers.txt> <fileWithWords.txt>"		

if __name__ == "__main__":
    main(sys.argv[1:])