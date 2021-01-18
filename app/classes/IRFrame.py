import evdev
from time import sleep

def calculatePercentage(val, minimum, maximum):

  return min(1,(max(0, val-minimum)/(maximum-minimum)))

class IRFrame(object):
  def __init__(self, devicePath, range):
    self.devicePath = devicePath
    self.range = range
    self.device = None
    self.values = {
      "xVal": 0,
      "yVal": 0,
      "xPercent":0.0,
      "yPercent":0.0
    }
  
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

  def setXVal(self,val):
    self.values["xVal"] = val
    self.values["xPercent"] = calculatePercentage(self.values["xVal"], self.range["xMin"], self.range["xMax"])
  
  def setYVal(self,val):
    self.values["yVal"] = val
    self.values["yPercent"] = calculatePercentage(self.values["yVal"], self.range["yMin"], self.range["yMax"])


