from pyparsing import *
import re

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

arithmeticTest = ["9",
		"1+2",
		"3*5",
		"2-2",
		"(2+5) * 3",
		"(3*5+1)+(2*2)*(a-1)",
		"(a*b)-x*y"
		]


statementTest = ["pen down",
		"pen up",
		"move forward",
		"move backward",
		"move(10,45)",
		"turn cw(90)",
		"turn ccw(30)",
		"put(10,50,45)",
		"for X=3*5 to 10 do\n pen down\n move(10,45)\nend"
		]
		

for t in arithmeticTest:
	print("Expression: %s" % t)	
	print("Parse: %s" % expression.parseString(t, parseAll = True))
	print 
	
print '##################\n'
	
for t in statementTest:
	print("Statement: %s" % t)
	print("Parse: %s" % input.parseString(t,parseAll=True))
	print
