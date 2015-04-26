import Translater
from pyparsing import *

###########Grammar###########
constant = Word(nums)
variable = Word(alphas)
operand = constant ^ variable

sign = oneOf('+ -')
multOp = '*'
addSubOp = oneOf('+ -')

expression = operatorPrecedence(operand, 
			[(sign, 1, opAssoc.RIGHT),
			(multOp, 2, opAssoc.LEFT),
			(addSubOp, 2, opAssoc.LEFT)]
			)

statement = Forward()
penDown = Literal("pen down")
penUp =  Literal("pen up")             
moveForward = Literal("move forward")
moveBackward = Literal("move backward")
move = "move(" + expression + "," + expression +")" 
turnCW = "turn cw("+ expression + ")"
turnCCW = "turn ccw(" + expression + ")"
put = "put(" + expression + "," + expression + "," + expression + ")"
statement = penDown ^  penUp ^  moveForward ^  moveBackward ^  move ^  turnCW ^  turnCCW ^  put
forLoop = "for"+variable+"="+ expression+"to"+expression+"do"+White('\n', exact=1)+OneOrMore(statement+White('\n', exact=1))+"end"
input = expression ^ statement ^ forLoop
###########Grammar###########

class Jtrans(Translater):

	def __init__(self):
		self.obj = None
		self.xPos = 0
		self.yPos = 0
		self.angle = 0
		self.penOn = False
		self.nextX = 0
		self.nextY = 0

	'''
	evaluate is used to calculate a arithmetic expression
	
	@expression the arithmetic expression 
	@variable if this variable is found , it is replaced by variableValue
	@variableValue the value that is meant to replace variable
	@return the value of the evaluated expression 
	'''
	def evaluate(self, expression, variable=None, variableValue=None):
		string =""
		for index in expression:
			index = variableValue if index == variable else index
			string += str(self.evaluate(index) if isinstance(index, list) else index)
		return eval(string)
	
	
	'''
	createSublists is used to create the statement lists outputted by for loops from createOutput
	
	@inputList the newline separated statement list
	@return a statement list of statements that are formatted as lists [[statement1], [statement2]]
	'''
	def createSublists(self, inputList):
		output = []
		sublist = []
		for x in inputList:
			sublist.append(x)
			if (x == '\n'):
				output.append(sublist)
				sublist = []
		output.append(sublist)
		return output
	'''
	createOutput is used to generate statement outputs that can be easily interpreted
	
	@parse the parsed expression that is to be converted to valid output
	@eval if true all the arithmetic expressions will be calculated else the will just be formatted strings
	@return a formatted output on the form: ['statement name', param1,param2...paramN]
	'''
	def createOutput(self, parse, eval=True):
		method = parse[0]
		
		output = []
		
		if(method == 'pen down'):
			output.append('pen down')
		elif(method == 'pen up'):
			output.append('pen up')
		elif(method == 'move forward'):
			output.append('move forward')
		elif(method == 'move backward'):
			output.append('move backward')
		elif(method == 'move('):
			steps = self.evaluate(parse[1]) if eval == True else parse[1]
			angle = self.evaluate(parse[3]) if eval == True else parse[3]
			output.append('move')
			output.append(steps)
			output.append(angle)
		elif(method == 'turn cw('):
			angle = self.evaluate(parse[1]) if eval == True else parse[1]
			output.append('turn cw')
			output.append(angle)
		elif(method == 'turn ccw('):
			angle = self.evaluate(parse[1]) if eval == True else parse[1]
			output.append('turn cw')
			output.append(angle)
		elif(method == 'put('):
			xpos = self.evaluate(parse[1]) if eval == True else parse[1]
			ypos = self.evaluate(parse[3]) if eval == True else parse[3]
			angle = self.evaluate(parse[5]) if eval == True else parse[5]
			output.append('put')
			output.append(xpos)
			output.append(ypos)
			output.append(angle)
		elif(method == 'for'):
			start = self.evaluate(parse[3]) #loop variable value
			end = self.evaluate(parse[5])  #end loop value, e.g. "...to 100" where 100 is end loop value
			startLoop = parse.index('do')+2 #beginning of statements in for loop
			endLoop = parse.index('end')-1 #end of statements in for loop
			statements = [] 
			test = parse[startLoop:endLoop]
			sublist = self.createSublists(parse[startLoop:endLoop]) #create loop statement sublist
			for statement in sublist:
				statements.append(self.createOutput(statement, False))
			output.append('for')
			output.append(str(parse[1])) #loop variable
			output.append(start) 
			output.append(end) 
			output.append(statements) #loop statements
			
		return output
	'''
	parse is used parse a input string and check if the string contains valid input
	
	@command the input string containing a possible valid command
	@return the command in formatted by createOutput
	'''
	def parse(self, command):
		parse = input.parseString(command,parseAll=True).asList()
		return self.createOutput(parse)
			
			
	def actionPerformed(self, event):
		command_list = self.obj.getCode().splitlines(True)
		for command in command_list:
			if(command.startswith('for')):
				index = command_list.index(command) +1
				stmt = command_list.pop(index)
				while(stmt != 'end'):
					command += stmt
					++index
					stmt = command_list.pop(index)
				command += 'end'
			print "Command: %s \n" % command
			print self.parse(command)
			print("####################################")
			##############################################
			self.execute(command, None, None)
			
	def execute(self, command, loopVariableName, loopVariableValue):
		for element in command:
			if element == loopVariableName:
				element = loopVariableValue
		key = command[0]
		if key == "pen down":
			self.penDown()
		elif key == "pen up":
			self.penUp()
		elif key == "move forward":
			self.moveForward()
		elif key == "move backward":
			self.moveBackward()
		elif key == "move":
			self.move(command[1], command[2])
		elif key == "turn cw":
			self.turnCW(command[1])
		elif key == "turn ccw":
			self.turnCCW(command[1])
		elif key == "put":
			self.put(command[1], command[2], command[3])
		elif key == "for":
			for command[1] in range(command[2], command[3]):
				for statement in command[4]:
					self.execute(statement, command[1], command[2])
		elif key == "end":
			break
				
	def penDown(self):
		penOn = True

	def penUp(self):
		penOn = False

	def moveForward(self):
		self.move(1, 0)
			
	def moveBackward(self):
		if self.angle < 22.5 or self.angle > 337.5:
			self.yPos += 1
			self.obj.setPixel(self.xPos, self.yPos)
		elif 67.5 > self.angle > 22.5:
			self.xPos -= 1
			self.yPos += 1
			self.obj.setPixel(self.xPos, self.yPos)
		elif 112.5 > self.angle > 67.5:
			self.xPos -= 1
			self.obj.setPixel(self.xPos, self.yPos)
		elif 157.5 > self.angle > 112.5:
			self.xPos -= 1
			self.yPos -= 1
			self.obj.setPixel(self.xPos, self.yPos)
		elif 202.5 > self.angle > 157.5:
			self.yPos -= 1
			self.obj.setPixel(self.xPos, self.yPos)
		elif 247.5 > self.angle > 202.5:
			self.xPos += 1
			self.yPos -= 1
			self.obj.setPixel(self.xPos, self.yPos)
		elif 292.5 > self.angle > 247.5:
			self.xPos += 1
			self.obj.setPixel(self.xPos, self.yPos)
		elif 337.5 > self.angle > 292.5:
			self.xPos += 1
			self.yPos += 1
			self.obj.setPixel(self.xPos, self.yPos)
			
	def move(self, steps, angle):
		self.turnCW(angle)
		numberOfPixels = steps*8
		degreesPerPixel = 360.0/numberOfPixels
		pixelList = []
		currentMinimumDegree = 0+degreesPerPixel/2
		maximumDegree = (0-(degreesPerPixel/2))%360
		pixelX = self.xPos
		pixelY = self.yPos - steps
		temp = 1
		firstPixel = self.Pixel(0, maximumDegree, currentMinimumDegree, pixelX, pixelY)
		pixelList.append(firstPixel)
		for x in range(1, numberOfPixels):
			if temp <= steps:
				temp += 1
				pixelX += 1
			elif temp <= steps*3:
				temp += 1
				pixelY += 1
			elif temp <= steps*5:
				temp += 1
				pixelX -= 1
			elif temp <= steps*7:
				temp += 1
				pixelY -= 1
			elif temp < steps *8:
				temp += 1
				pixelX += 1
			maximumDegree = currentMinimumDegree + degreesPerPixel
			newPixel = self.Pixel(x, currentMinimumDegree, maximumDegree, pixelX, pixelY)
			pixelList.append(newPixel)
			currentMinimumDegree += degreesPerPixel
		
		for pixel in pixelList:
			if pixel.pixelNumber == 0:
				if pixel.max > self.angle or self.angle > pixel.min:
					self.obj.setPixel(pixel.x, pixel.y)
					self.nextX = pixel.x
					self.nextY = pixel.y
			elif pixel.max > self.angle > pixel.min:
				self.obj.setPixel(pixel.x, pixel.y)
				self.nextX = pixel.x
				self.nextY = pixel.y
		
		if steps > 1:
			self.recursiveMove(steps-1)
		
		self.xPos = self.nextX
		self.yPos = self.nextY
		self.put(self.xPos, self.yPos, self.angle)
		
	def recursiveMove(self, steps):# Recursive move fuction
		numberOfPixels = steps*8
		degreesPerPixel = 360.0/numberOfPixels
		pixelList = []
		currentMinimumDegree = 0+degreesPerPixel/2
		maximumDegree = (0-(degreesPerPixel/2))%360
		pixelX = self.xPos
		pixelY = self.yPos - steps
		temp = 1
		firstPixel = self.Pixel(0, maximumDegree, currentMinimumDegree, pixelX, pixelY)
		pixelList.append(firstPixel)
		for x in range(1, numberOfPixels):
			if temp <= steps:
				temp += 1
				pixelX += 1
			elif temp <= steps*3:
				temp += 1
				pixelY += 1
			elif temp <= steps*5:
				temp += 1
				pixelX -= 1
			elif temp <= steps*7:
				temp += 1
				pixelY -= 1
			elif temp < steps *8:
				temp += 1
				pixelX += 1
			maximumDegree = currentMinimumDegree + degreesPerPixel
			newPixel = self.Pixel(x, currentMinimumDegree, maximumDegree, pixelX, pixelY)
			pixelList.append(newPixel)
			currentMinimumDegree += degreesPerPixel
		
		for pixel in pixelList:
			if pixel.pixelNumber == 0:
				if pixel.max > self.angle or self.angle > pixel.min:
					self.obj.setPixel(pixel.x, pixel.y)
			elif pixel.max > self.angle > pixel.min:
				self.obj.setPixel(pixel.x, pixel.y)
		
		if steps > 1:
			self.recursiveMove(steps-1)

	def turnCW(self, angle):
		self.angle = (self.angle + angle)%360

	def turnCCW(self, angle):
		self.angle = (self.angle - angle)%360
	
	def put(self, newXPos, newYPos, newAngle):
		self.xPos = newXPos
		self.yPos = newYPos
		self.angle = newAngle

	def setDYPL( self, obj ):
		self.obj = obj  
		
	class Pixel:
		def __init__(self, pixelNumber, minimumDegree, maximumDegree, pixelX, pixelY):
			self.pixelNumber = pixelNumber
			self.min = minimumDegree
			self.max = maximumDegree
			self.x = pixelX
			self.y = pixelY
			
if __name__ == '__main__':
    import DYPL
    DYPL(Jtrans())
