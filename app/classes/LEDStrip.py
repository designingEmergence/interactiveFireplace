from rpi_ws281x import *
from time import sleep

def wheel(pos):
  """Generate rainbow colors across 0-255 positions."""
  if pos < 85:
    return Color(pos * 3, 255 - pos * 3, 0)
  elif pos < 170:
    pos -= 85
    return Color(255 - pos * 3, 0, pos * 3)
  else:
    pos -= 170
    return Color(0, pos * 3, 255 - pos * 3)

def colorToRGB(color):
  return color >> 16, color >> 8 & 255, color & 255

def averageRGBColors(colors):
  red = 0
  green = 0
  blue = 0
  for color in colors:
    red += color[0]
    blue += color[1]
    green += color[2]
  
  red = int(red/len(colors))
  green = int(green/len(colors))
  blue = int(blue/len(colors))
  
  return Color(red, blue, green)

class LEDStrip(object):
  def __init__(self, ledCount, ledPin, bL, bR, tL, tR, maxBrightness=255, defaultColor=Color(255,255,255)):
    self.ledCount = ledCount
    self.ledPin = ledPin
    self.bottomLeft = bL
    self.bottomRight = bR
    self.topLeft = tL
    self.topRight = tR
    self.ledFreq = 800000
    self.ledDMA = 10
    self.maxBrightness = maxBrightness
    self.ledSignalInvert = False
    self.ledChannel = 0
    self.defaultColor = defaultColor
    self.strip = Adafruit_NeoPixel(self.ledCount, self.ledPin, self.ledFreq, self.ledDMA, self.ledSignalInvert, self.maxBrightness, self.ledChannel)
    self.strip.begin()
    self.animate = False

  def show(self):
    self.strip.show()
  
  def stopAnimation(self):
    #print('stop animation')
    self.animate = False

  def calculatePixel(self, percentVal, minimum, maximum):
    scale = maximum-minimum
    pixelVal = percentVal*scale + minimum
    return int(pixelVal)

  def setStripColor(self, color=Color(0,0,0), show=False):
    for i in  range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
    if show:
      self.strip.show()
  
  def setSegmentColor(self, start, end, color):
    for i in range(start, end):  
        self.strip.setPixelColor(i,color)
    
  def colorWipe(self, color, wait_ms=5):
    for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, color)
        self.strip.show()
        sleep(wait_ms/1000.0)

  def showRainbow(self,offset=0):
    for i in range(self.strip.numPixels()):
      color = wheel(int(i*256/self.strip.numPixels()+offset) & 255)
      self.strip.setPixelColor(i,color)
    self.strip.show()
  
  def theaterChase(self, color=Color(90,50,20), wait_ms=50):
    print('theater chase')
    while self.animate:
      for q in range(3):
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, color)
        self.strip.show()
        sleep(wait_ms/1000.0)
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, 0)

  def animatingRainbow(self, wait_ms=30):
    print('rainbow')
    while self.animate:
      for j in range(256):
        if self.animate == False:
          break
        self.showRainbow(j)
        sleep(wait_ms/1000.0)
  
  def smooth(self, ledA, ledB, ledC):
      colorA = colorToRGB(self.strip.getPixelColor(ledA))
      colorB = colorToRGB(self.strip.getPixelColor(ledB))
      colorC = colorToRGB(self.strip.getPixelColor(ledC))
      return averageRGBColors([colorA, colorB, colorC])
  
  
  def smoothStrip(self, wait_ms=10):
    print('smooth strip')
    while self.animate:
      for i in range(self.strip.numPixels()):
        if i == 0:
          c = self.smooth(self.strip.numPixels()-1,i, i+1)
        elif i == self.strip.numPixels()-1:
          c = self.smooth(i-1,i,0)
        else:
          c = self.smooth(i-1,i,i+1)
        
        self.strip.setPixelColor(i,c)

      self.strip.show()
      sleep(wait_ms/1000.0)

  def showAllSegments(self):
    self.setSegmentColor(0, self.bottomLeft, Color(255,0,0))
    self.setSegmentColor(self.bottomLeft, self.topLeft, Color(0,255,0))
    self.setSegmentColor(self.topLeft, self.topRight, Color(0,0,255))
    self.setSegmentColor(self.topRight, self.bottomRight, Color(255,255,255))      
    self.strip.show()
  
  def showXYPosition(self,x, y, color=Color(255,0,255)):
    bottomX = self.calculatePixel(1-x, 0, self.bottomLeft)
    topX = self.calculatePixel(x, self.topLeft, self.topRight)
    rightY = self.calculatePixel(1-y, self.bottomRight, self.topRight)
    leftY = self.calculatePixel(y, self.topLeft, self.bottomLeft)
    self.strip.setPixelColor(bottomX, color)
    self.strip.setPixelColor(topX, color)
    self.strip.setPixelColor(rightY, color)
    self.strip.setPixelColor(leftY, color)
  
  def showEdgeProximity(self, x, y, distanceThreshold):

    #distance threshold from 0 to 1. The higher the threshold the closer you have to be to that edge
    bL = max(0,(1-x)-distanceThreshold)
    bR = max(0,x-distanceThreshold)
    bB = max(0,y-distanceThreshold)
    bT = max(0,(1-y)-distanceThreshold)
    print(bL)


    colorLeft = Color(int(bL*100),int(bL*100),int(bL*40))
    colorRight = Color(int(bR*100),int(bR*100),int(bR*40))
    colorBottom = Color(int(bB*100),int(bB*100),int(bB*40))
    colorTop = Color(int(bT*100),int(bT*100),int(bT*40))

    self.setSegmentColor(self.bottomLeft, self.topLeft, colorLeft)
    self.setSegmentColor(self.topRight, self.bottomRight, colorRight)
    self.setSegmentColor(0, self.bottomLeft, colorBottom) 
    self.setSegmentColor(self.topLeft, self.topRight, colorTop)