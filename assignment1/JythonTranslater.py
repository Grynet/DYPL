import Translater

class Jtrans(Translater):

	def __init__(self):
		self.obj = None
		self.xPos = 0
		self.yPos = 0
		self.angle = 0
		self.penOn = False
		self.nextX = 0
		self.nextY = 0

	def parse(self, command):
		print(command)

	def actionPerformed(self, event):
		self.put(270, 150, 180)
		for x in range(0, 180):#changed from 180
			self.move(4, 2)
		
		self.put(200, 80, 180)
		for x in range(0, 45):
			self.move(1, 8)

		self.put(100, 80, 180)
		for x in range(0, 45):
			self.move(1, 8)

		self.put(180, 150, 180)
		for x in range(0, 45):
			self.move(2, 4)

		for x in range(0, 100):
			self.put(100+x, 190, 230-x*2)
			self.move(10, 0)
			
		self.put(150, 150, 0)
		self.move(100, 10)
		self.put(150, 150, 0)
		self.move(100, 0)

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
		
	def recursiveMove(self, steps):
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