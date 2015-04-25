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

	def parse(self, command):
		print ("Command: %s" % command)
		print("Parse: %s" % input.parseString(command,parseAll=True))

	# def actionPerformed(self, event):
		# command_list = self.obj.getCode().splitlines()
		# for command in command_list:
			# self.parse(command)
		# print ("ActionPerformed executed")

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
			self.parse(command)
		print("####################################")


	def setDYPL( self, obj ):
		self.obj = obj  
		print("Object set")     

if __name__ == '__main__':
    import DYPL
    DYPL(Jtrans())
