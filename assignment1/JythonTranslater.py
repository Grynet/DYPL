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

	def evaluate(self, expression, variable=None, variableValue=None):
		string =""
		for index in expression:
			index = variableValue if index == variable else index
			string += str(self.evaluate(index) if isinstance(index, list) else index)
		return eval(string)
		
	def createSublist(self,list):
		current = []
		for element in list:
			if element=="\n":
				yield current
				current = []
			else:
				current.append(element)
		yield current
		
	def magicsplit(self,l, *splitters):
		return [subl for subl in self.createSublist(l) if subl]

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
			print "Angle: %s" % angle
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
			print "Test: %s" % test
			sublist = self.magicsplit(parse[startLoop:endLoop]) #create loop statement sublist
			for statement in sublist:
				statements.append(self.createOutput(statement, False))
			output.append('for')
			output.append(str(parse[1])) #loop variable
			output.append(start) 
			output.append(end) 
			output.append(statements) #loop statements
			
		return output

	def parse(self, command):
		parse = input.parseString(command,parseAll=True).asList()
		print "Parse: %s" % parse
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


	def setDYPL( self, obj ):
		self.obj = obj  
		print("Object set")     

if __name__ == '__main__':
    import DYPL
    DYPL(Jtrans())
