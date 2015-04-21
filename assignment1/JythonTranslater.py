import Translater

class Jtrans(Translater):
	
	def __init__(self):
		self.obj = None

	def parse(self, command):
		print(command)

	def actionPerformed(self, event):
		command_list = self.obj.getCode().splitlines()
		for command in command_list:
			self.parse(command)
		print ("ActionPerformed executed")

	def setDYPL( self, obj ):
		self.obj = obj  
		print("Object set")     

if __name__ == '__main__':
    import DYPL
    DYPL(Jtrans())
