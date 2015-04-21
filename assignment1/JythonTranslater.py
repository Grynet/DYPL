import Translater

class Jtrans(Translater):

    def __init__(self):
        self.obj = None

    def actionPerformed(self, event):
		print(self.obj.getCode())
		print ("efter")
		
    def setDYPL( self, obj ):
		self.obj = obj  
		print("Object set")		       

if __name__ == '__main__':
    import DYPL
    DYPL(Jtrans())
