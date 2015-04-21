'''
Created on 21 apr 2015

@author: Tobias
'''
import Translater
from java.awt.event import ActionEvent
'''
Might need to change the name of the class to JythonTranslater$Jtrans.
'''
class MyTranslater(Translater):
    def __init__(self):
        self.object = None
		self.xPos = 0
		self.yPos = 0
		self.angle = 0
        
    def actionPerformed(self, event):
        inputText = object.getCode()
		parse(inputText)
		
        
    def setDYPL(self, obj):
        self.object = obj
		
	def parse(inputText):
		result = re.match(r".*?\n", inputText)
		inputText.strip(r".*?\n")
		while(result != r".*?\n$")
			result = re.match(r".*?\n", inputText)
			if (re.match(r"", result))
			inputText.strip(r".*?\n")

			
			
			
			
			
			
        