# import time
# import sys
# from socket import *
# from rpi_ws281x import *
# import argparse
# from threading import Timer

import math
from classes.IRFrame import IRFrame
from classes.AudioSocket import AudioSocket

#IR Frame Settings
IRFramePath = '/dev/input/by-id/usb-Multi_touch_Multi_touch_overlay_device_68791EBC0D32-event-if01'
frameRange = {
  "xMin": 300,
  "yMin":300,
  "xMax":30000,
  "yMax":30000
}



if __name__ == '__main__':
  
  frame = IRFrame(IRFramePath, frameRange)
  frameEvents = frame.start()

  audio = AudioSocket(9800)
  audio.start()

  try:
    for event in frameEvents.read_loop():
      #print(event)
      if event.code == 53:
        frame.setXVal(event.value)
        note = int(math.ceil(frame.xPercent*100))

      elif event.code == 54:
        frame.setYVal(event.value)
        vol = int(math.ceil((1-frame.yPercent)*100)/2 + 20)
      
      elif event.code == 0:
        audio.sendNote(2,note,vol)
  
  except KeyboardInterrupt:
    if args.clear:
      print("clear")