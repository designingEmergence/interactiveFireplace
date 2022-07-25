from socket import *
from time import sleep
from .timers import RepeatedTimer

class AudioSocket(object):

  def __init__(self, port):
    self.port = port
    self.host = "localhost"
    self.audioSocket = socket(AF_INET, SOCK_STREAM)
    self.socketBlock = False
    self.blockingTimer = None
  
  def connectToSocket(self, serverHost, serverPort, tries):
    for x in range(0,tries):
      print("connecting to " + str(serverHost) + ":" + str(serverPort))
      try:
        self.audioSocket.connect((serverHost, serverPort))
        break
      except:
        print('error connecting to audio socket')
        sleep(3)
        
  def start(self):
    self.connectToSocket(self.host, self.port, 10)
    self.blockTimer = RepeatedTimer(.1, self.resetSocketBlocker)
  
  def resetSocketBlocker(self):
    self.socketBlock = False

  def loadSoundFont(self, file):
    self.audioSocket.send(("load " + file + "\n").encode())
    print('loading file '+ file)
  
  def sendNote(self, val, note, vol):
    if self.socketBlock == False:
      self.audioSocket.send(("noteon " + str(val) + " " + str(note) + " " + str(vol)  + " \n").encode())
      self.socketBlock = True
      print('sending note')
    
  def sendReset(self):
    if self.socketBlock == False:
      self.audioSocket.send(("reset"+ " \n" ).encode())
      self.socketBlock = True