import evdev

device = evdev.InputDevice('/dev/input/event0') #what happens if this changes. Can look through all event files and find correct one.
print(device)


for event in device.read_loop():
    #print(event)
    
    if event.code == 53:
        xVal = event.value
        #print('X: ' + str(xVal))
    
    elif event.code == 54:
        yVal = event.value
        #print('Y: ' + str(yVal))
    
    elif event.code == 0:
        print('X: ' + str(xVal) + ' Y: ' + str(yVal))
    
