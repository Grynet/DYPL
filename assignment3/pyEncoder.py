DICT = {
	"6":6, "k":7, "v":6, "7":7, "l":8, "a":5, "w":2, 
	"8":8, "b":7, "m":5, "x":2, "9":9, "c":6, "y":3, 
	"n":1, "z":9, "o":8, "d":3, "0":0, "p":8, "e":0, 
	"1":1, "f":4, "q":1, "2":2, "g":9, "r":2, "3":3, 
	"h":9, "s":3, "4":4, "i":6, "t":4, "5":5, "u":7, 
	"j":1
}

words = []

results = []

def wordToNumber(word):
	return ''.join(str(DICT[e]) for e in list(word))

def readWordFile(filePath):
	with open(filePath, 'r') as theFile:
		return [word.rstrip('\n').lower() for word in theFile]

def match(number, word):
	return wordToNumber(word) == number


def findMatches(number, wordFilePath):
	global words
	words = readWordFile(wordFilePath)
	encode(number, "")	

def encode(number, encoding):
	global words
	global results
	if number == "":
		results.append("%s : %s" %(wordToNumber(encoding.replace(" ","")), encoding))
	else:
		for word in words:			
			if len(word) <= len(number):
				wordAsNumber = wordToNumber(word)
				if number.startswith(wordAsNumber):
					if(encoding == ""):
						newEncoding = encoding + word
					else:
						newEncoding = encoding + " %s" % (word)	
					newNumber = number[len(word):]	
					encode(newNumber, newEncoding)	


