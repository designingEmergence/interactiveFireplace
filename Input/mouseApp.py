import struct

f = open( "/dev/input/mice", "rb" );

while 1:
    data = f.read(3)
    print(struct.unpack('3b',data)) 