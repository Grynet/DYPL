from pyparsing import *

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

test = ["9",
		"1+2",
		"3*5",
		"2-2",
		"(2+5) * 3",
		"(3*5+1)+(2*2)*(a-1)",
		"(a*b)-x*y"
		]

for t in test:
	print("Expression: %s" % t)	
	print("Parse: %s" % expression.parseString(t))
	print