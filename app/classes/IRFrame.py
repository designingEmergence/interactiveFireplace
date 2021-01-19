import evdev
from time import sleep

def calculatePercentage(val, minimum, maximum):

  return min(1,(max(0, val-minimum)/(maximum-minimum)))

class IRFrame(object):
  def __init__(self, devicePath, range):
    self.devicePath = devicePath
    self.range = range
    self.device = None
    
    self.xVal = 0
    self.yVal = 0
    self.xPercent = 0.0
    self.yPercent = 0.0

  
  def loadDevice(self,devicePath, attempts):
    for x in range(0, attempts):
      try:
        dev = evdev.InputDevice(devicePath)
        print(dev)
        return dev
      except Exception:
        print('no file found')
        sleep(2)

  def start(self):
    self.device = self.loadDevice(self.devicePath, 4)
    return self.device

  def setXVal(self, val):
    self.xVal = val
    self.xPercent = calculatePercentage(self.xVal, self.range["xMin"], self.range["xMax"])
  
  def setYVal(self,val):
    self.yVal = val
    self.yPercent = calculatePercentage(self.yVal, self.range["yMin"], self.range["yMax"])


