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

	def evaluate(self, expression):
		string =""
		for index in expression:
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
	
	def variableReplace(self, inputList, variable, value):
		output = []
		for x in inputList:
			if (isinstance(x, list)):
				for y in self.variableReplace(x, variable, value):
					output.append(y)
			elif(x == variable):
				output.append(value)
			else:
				output.append(x)
		return output

	def createOutput(self, parse):
		method = parse[0]
		
		if(method == 'pen down'):
			return ['pen down']
		elif(method == 'pen up'):
			return ['pen up']
		elif(method == 'move forward'):
			return ['move forward']
		elif(method == 'move backward'):
			return ['move backward']
		elif(method == 'move('):
			steps = self.evaluate(parse[1])
			angle = self.evaluate(parse[3])
			return ['move', steps, angle]
		elif(method == 'turn cw('):
			angle = self.evaluate(parse[1])
			return ['turn cw', angle]
		elif(method == 'turn ccw('):
			angle = self.evaluate(parse[1])
			return ['turn ccw', angle]
		elif(method == 'put('):
			xpos = self.evaluate(parse[1])
			ypos = self.evaluate(parse[3])
			angle = self.evaluate(parse[5])
			return ['put', xpos, ypos, angle]
		elif(method == 'for'):
			start = self.evaluate(parse[3]) #loop variable value
			end = self.evaluate(parse[5])  #end loop value, e.g. "...to 100" where 100 is end loop value
			parse = [str(start) if(x == parse[1]) else x for x in parse] #loop variable to value
			startLoop = parse.index('do')+2 #beginning of statements in for loop
			endLoop = parse.index('end')-1 #end of statements in for loop
			statements = [] 
			sublist = self.magicsplit(parse[startLoop:endLoop]) #create loop statement sublist
			for statement in sublist:
				statements.append(self.createOutput(statement))
			return ['for', start, end, statements]

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


	def setDYPL( self, obj ):
		self.obj = obj  
		print("Object set")     

if __name__ == '__main__':
    import DYPL
    DYPL(Jtrans())
