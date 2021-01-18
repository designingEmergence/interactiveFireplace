import evdev
import time
import sys
from socket import * 
import math
from rpi_ws281x import *
import argparse
from threading import Timer

#AUDIO

serverHost = "localhost"
serverPort = 9800
s = socket(AF_INET, SOCK_STREAM)
socketBlock = False

#device Path
devicePath = '/dev/input/by-id/usb-Multi_touch_Multi_touch_overlay_device_68791EBC0D32-event-if01'

# Raw IR Frame Values
xMin = 300
yMin = 300
xMax = 30000
yMax = 30000

# LED strip configuration:
LED_COUNT      = 308     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

maxBrightness = 100
defaultColor = Color(255,255, 255)
edgeProximity = 0.6

#LED NUMBER
bottomLeft = 308
bottomRight = 78
topRight = 153
topLeft = 228

strip = None

class LightOffTimer(object):
    def __init__(self, offTime, strip):
        self.offTime = offTime
        self.strip = strip
        self.enabled = False
        self._timer = None
    
    def start(self):
        if not self.enabled:
            #print('start off timer')
            self._timer= Timer(self.offTime, removeHand)
            self._timer.start()
            self.enabled = True

    def stop(self):
        if self.enabled:
            #print('cancel off timer')
            self._timer.cancel()
            self.enabled = False
        

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def resetSocketBlocker():
    global socketBlock
    socketBlock = False
    #print("RESET SOCKET BLOCK")

def removeHand(): #define what happens if hand is removed
    clearStrip(strip=strip, show=True)
    sendReset()

def sendNote(val, note, vol):
    global socketBlock
    global s
    if socketBlock == False:
        #print("noteon " + str(val) + " " + str(note) + " " + str(vol))
        s.send(("noteon " + str(val) + " " + str(note) + " " + str(vol)  + " \n").encode())
        socketBlock = True

def sendReset():
    global socketBlock
    global s
    if socketBlock == False:
        print("reset")
        s.send(("reset"+ " \n" ).encode())
        socketBlock = True
  
#IR Frame device

def loadDevice():
    for x in range(0, 4):  # try 4 times
        try:
            dev = evdev.InputDevice(devicePath) #what happens if this changes. Can look through all event files and find correct one.
            print(dev)
            return dev
        except Exception:
            print('no file found')
            time.sleep(2) 
            #loadDevice()

def connectToSocket(serverHost, serverPort):
    global s
    #s.connect((serverHost, serverPort))
    for x in range(0,10):
        print("connecting to " + str(serverHost) + ":" + str(serverPort))
        try:            
            s.connect((serverHost, serverPort))
            break
        except:
            print('error connecting')
            time.sleep(3)

# Define functions which animate LEDs in various ways.

def clearStrip(strip, color=Color(0,0,0), show=False):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    if show:
        print("clearing strip")
        strip.show()

def colorWipe(strip, color, wait_ms=5):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def showSegments(strip):
    for i in range(0, bottomRight):
        strip.setPixelColor(i, Color(255,0,0))
    
    for i in range(bottomRight, topRight):
        strip.setPixelColor(i, Color(0,255,0))

    for i in range(topRight, topLeft):
        strip.setPixelColor(i, Color(0,0,255))
    
    for i in range(topLeft, bottomLeft):
        strip.setPixelColor(i, Color(80,80,80))
    
    strip.show()

def setSegmentBrightness(strip, start, end, brightnessNorm):
    #print(maxBrightness*brightnessNorm)
    b = max(0, brightnessNorm - (edgeProximity))
    for i in range(start, end):  
        strip.setPixelColor(i,Color(int(maxBrightness*b),int(maxBrightness*b),int(maxBrightness*b)))

def calculatePixel(val, min, max):
    scale = max-min
    pixelVal = val * scale + min
    return int(pixelVal)

def showXYPosition(x, y, color=Color(100,0,100)):
    
    bottomX = calculatePixel(x, 0, bottomRight)
    topX = calculatePixel(1-x, topRight, topLeft)
    rightY = calculatePixel(1-y, bottomRight, topRight)
    leftY = calculatePixel(y, topLeft, bottomLeft)
    strip.setPixelColor(bottomX, color)
    strip.setPixelColor(topX, color)
    strip.setPixelColor(rightY, color)
    strip.setPixelColor(leftY, color)

    #print('bottom: ' + str(bottomX) + ' top: '+ str(topX) + ' left: ' + str(leftY) + ' right: ' + str(rightY))

def showEdgeProximity(x,y):
    setSegmentBrightness(strip, topLeft, bottomLeft, 1-x) #left
    setSegmentBrightness(strip, bottomRight, topRight, x) #right
    setSegmentBrightness(strip, 0, bottomRight, y) #bottom
    setSegmentBrightness(strip, topRight, topLeft, 1-y)  #top

# Main program logic follows:
if __name__ == '__main__':

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    #load IR frame
    device = loadDevice()

    #connect to audio
    connectToSocket(serverHost, serverPort)
    socketTimer = RepeatedTimer(.1, resetSocketBlocker)

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    #Light Off Timer
    offTimer = LightOffTimer(12, strip)

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    showSegments(strip)
    try:
        for event in device.read_loop():
            #print(event)
            if event.code == 53:
                xVal = event.value
                xPercent = min(1,(max(0, xVal-xMin)/(xMax-xMin)))
                note = int(math.ceil(xPercent*100))
                offTimer.stop()
            
            elif event.code == 54:
                yVal = event.value
                yPercent = min(1,(max(0, yVal-yMin)/(yMax-yMin))) 
                vol = int(math.ceil((1-yPercent)*100)/2 + 20)
            
            elif event.code == 0:
                #print('X: ' + str(round(xPercent,2)) + ' Y: ' + str(round(yPercent,2)))
                clearStrip(strip)
                #showEdgeProximity(xPercent, yPercent)
                showXYPosition(xPercent, yPercent)
                strip.show()
                offTimer.start()
                sendNote(2,note,vol)
            
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)



