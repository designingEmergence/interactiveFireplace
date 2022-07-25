import math
import argparse
from threading import Thread
from rpi_ws281x import Color
from classes.IRFrame import IRFrame
from classes.AudioSocket import AudioSocket
from classes.LEDStrip import LEDStrip
from classes.timers import NoEventTimer
from classes.MovingPoint import MovingPoint

#IR Frame Settings
IRFramePath = '/dev/input/by-id/usb-Multi_touch_Multi_touch_overlay_device_68791EBC0D32-event-if01'
frameRange = {
  "xMin": 300,
  "yMin":300,
  "xMax":30000,
  "yMax":30000
}

#LED strip settings
ledCount = 308
ledPin = 18
ledBottomLeft = 308
ledBottomRight = 78
ledTopRight = 153
ledTopLeft = 228

frame = IRFrame(IRFramePath, frameRange)
audio = AudioSocket(9800)
ledStrip = LEDStrip(ledCount, ledPin, ledBottomLeft, ledBottomRight, ledTopLeft, ledTopRight,maxBrightness=20)

target = MovingPoint(vel=0.002) 

def screensaver():
  #ledStrip.theaterChase(color=Color(90,50,20), wait_ms=100)
  #ledStrip.animatingRainbow(100)
  #ledStrip.smoothStrip()
  ledStrip.setStripColor(show=True)

def removeHand(): #define what happens if hand is removed
  ledStrip.animate = True
  animation = Thread(target=screensaver, args=())
  animation.start()
  audio.sendReset()
  print("hand removed")

def draw(): #constantly running function
  while True:
    ledStrip.setStripColor(show=False)
    target.update()
    ledStrip.showXYPosition(frame.xPercent, frame.yPercent, color=Color(255,255,100))
    ledStrip.showXYPosition(target.xPos, target.yPos, color=Color(100,100,100))
    ledStrip.show()
    if target.changedVelocity == True:
      print('change')
      #audio.sendNote(2,60,127)
      target.changedVelocity = False
    

if __name__ == '__main__':
  
  ledStrip.setStripColor(show=True)
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
  args = parser.parse_args()
  
  frameEvents = frame.start()

  audio.start()
  audio.loadSoundFont('selected/solarwind.sf2')

  drawThread = Thread(target=draw, args=())
  drawThread.start()

  removeHand()
  offTimer = NoEventTimer(3)

  try:
    for event in frameEvents.read_loop():
      #print(event)
      if event.code == 53:
        if ledStrip.animate:
          ledStrip.stopAnimation()

        offTimer.cancel()
        frame.setXVal(event.value)
        note = int(math.ceil(frame.xPercent*100))

      elif event.code == 54:
        frame.setYVal(event.value)
        vol = int(math.ceil((1-frame.yPercent)*100)/2 + 77) # vol max 127

      #elif event.code == 0:
        #ledStrip.setStripColor(show=False)
        #ledStrip.showXYPosition(frame.xPercent, frame.yPercent, color=Color(255,255,100))
        #ledStrip.show()
        audio.sendNote(2,note,vol)
        #offTimer.start(removeHand)        
  
  except KeyboardInterrupt:
    if args.clear:
      print("clear")