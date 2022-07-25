import random

class MovingPoint(object):

  def __init__(self, vel=0.003, velChangePercent=0.002):
    self.xPos = 0.5
    self.yPos = 0.5
    self.maxVel = vel
    self.velChangePercent = velChangePercent
    self.xVel = vel * random.choice([-1,1]) 
    self.yVel = vel * random.choice([-1,1])
    self.changedVelocity = False
      
  def update(self):
    changeVelocity = random.uniform(0,1)
    if changeVelocity < self.velChangePercent:
      self.changeVelocity()

    self.checkEdges()
    self.xPos += self.xVel
    self.yPos += self.yVel
  
  def changeVelocity(self):
    #right not it only changes direction. If want to change velocity, then multiply by (-) random new velocity
    randNum = random.uniform(0,1)
    if randNum < 0.4:
      self.xVel *= -1 
      self.changedVelocity = True
    
    elif randNum < 0.8:
      self.yVel *= -1
      self.changedVelocity = True

    else:
      self.xVel *= -1
      self.yVel *= -1
  
  def checkEdges(self):
    if self.xPos > 1 or self.xPos < 0 :
      self.xVel *= -1
    
    if self.yPos > 1 or self.yPos < 0:
      self.yVel *= -1
