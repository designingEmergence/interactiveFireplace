from rpi_ws281x import *
from time import sleep

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
    print('stop animation')
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
  
  def theaterChase(self, color, wait_ms=50, iterations=10):
    print('theater chase')
    while self.animate:
      for q in range(3):
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, color)
        self.strip.show()
        sleep(wait_ms/1000.0)
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, 0)

  def showAllSegments(self):
    self.setSegmentColor(0, self.bottomRight, Color(255,0,0))
    self.setSegmentColor(self.bottomRight, self.topRight, Color(255,0,0))
    self.setSegmentColor(self.topRight, self.topLeft, Color(255,0,0))
    self.setSegmentColor(self.topLeft, self.bottomLeft, Color(255,0,0))      
    self.strip.show()
  
  def showXYPosition(self,x, y, color=Color(100,0,100)):
    bottomX = self.calculatePixel(x, 0, self.bottomRight)
    topX = self.calculatePixel(1-x, self.topRight, self.topLeft)
    rightY = self.calculatePixel(1-y, self.bottomRight, self.topRight)
    leftY = self.calculatePixel(y, self.topLeft, self.bottomLeft)
    self.strip.setPixelColor(bottomX, color)
    self.strip.setPixelColor(topX, color)
    self.strip.setPixelColor(rightY, color)
    self.strip.setPixelColor(leftY, color)
  
  def showEdgeProximity(self, x, y, distanceThreshold):
    bL = max(0,(1-x)-distanceThreshold)
    bR = max(0,x-distanceThreshold)
    bB = max(0,y-distanceThreshold)
    bT = max(0,(1-y)-distanceThreshold)

    colorLeft = Color(int(bL*100),int(bL*100),int(bL*100))
    colorRight = Color(int(bR*100),int(bR*100),int(bR*100))
    colorBottom = Color(int(bB*100),int(bB*100),int(bB*100))
    colorTop = Color(int(bT*100),int(bT*100),int(bT*100))

    self.setSegmentColor(self.topLeft, self.bottomLeft, colorLeft)
    self.setSegmentColor(self.bottomRight, self.topRight, colorRight)
    self.setSegmentColor(0, self.bottomRight, colorBottom)
    self.setSegmentColor(self.topRight, self.topLeft, colorTop)