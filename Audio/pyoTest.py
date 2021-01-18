from pyo import *
s = Server(duplex=0)
s.setInOutDevice(0)
s.boot()
s.start()
a = Sine(mul=0.01).out()
s.gui(locals())