import Translater

class Jtrans(Translater):

    def __init__(self):
        self.obj = None

	def parse(self, element):
		print(element)
		
    def actionPerformed(self, event):
		list = self.obj.getCode().splitlines()
		for element in list:
			self.parse(element)
		
    def setDYPL( self, obj ):
		self.obj = obj  
		print("Object set")		       

if __name__ == '__main__':
    import DYPL
    DYPL(Jtrans())
