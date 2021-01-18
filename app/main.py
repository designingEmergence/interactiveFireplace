# import time
# import sys
# from socket import *
# import math
# from rpi_ws281x import *
# import argparse
# from threading import Timer

from classes.IRFrame import IRFrame

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

  try:
    for event in frameEvents.read_loop():
      #print(event)
      if event.code == 53:
        frame.setXVal(event.value)
      
      elif event.code == 54:
        frame.setYVal(event.value)
      
      elif event.code == 0:
        print(frame.values)
  
  except KeyboardInterrupt:
    if args.clear:
      print("clear")