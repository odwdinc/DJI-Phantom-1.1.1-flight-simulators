import serial,struct
import logging

logging.basicConfig()
ser = ""

start1="\x55\xaa\x55\xaa\x20\x00\x01\x00\x00\xb1\x0f\x00\x80\x00\xdd\x00\x30\xf7\x73\x04\x34\x61\xe5\x00\x68\x01\xf2\x00\x30\xf7\x08\x00\x00\xf7\x66\x1c"
start2="\x55\xaa\x55\xaa\x1e\x00\x01\x00\x00\x01\x01\x00\x80\x00\x73\x04\x34\x61\xe5\x00\x68\x01\xf2\x00\x30\xf7\x08\x00\x00\xf7\x66\x1c\x6b\xd5"

status="\x55\xaa\x55\xaa\x1e\x00\x01\x00\x00\x1c\x02\x00\x80\x00\x00\x675\x00\x00\x00\xd0\xed\xd5\x03\xd0\xed\xd5\x03\xbb\x79\xe0\x00\x36\x6b"

ack = "\x55\xaa\x55\xaa"

def strt(ComPort):
    global ser
    print "Whatting on ComPort: "+ComPort
    while True:
        try:
            ser = serial.Serial(ComPort, rtscts=1)
        except serial.serialutil.SerialException:
            pass
        else:
            break
    ser.baudrate = 115200
    print "conected to : "+ ser.name

    ser.write(start1)
    ser.write(start2)
    s = ser.read(4)
    if s == ack:
        s = ser.read(63)
        #print  ':'.join(x.encode('hex') for x in s)
        s = ser.read(4)
        if s == ack:
            s = ser.read(31)
            return 1
    return 0


def syinc():

    ser.write(status)
    
    s = ser.read(4)
    if s == ack:
        s = ser.read(27)
        roll = struct.unpack( "h", ser.read(2)[0:2] )[0]
        s = ser.read(2)
        throtal = struct.unpack( "h", ser.read(2)[0:2] )[0]
        s = ser.read(2)
        pitch = struct.unpack( "h", ser.read(2)[0:2] )[0]
        s = ser.read(2)
        Yaw = struct.unpack( "h", ser.read(2)[0:2] )[0]
        s = ser.read(2)
        mode = struct.unpack( "h", ser.read(2)[0:2] )[0]
        s = ser.read(2)
        gps = struct.unpack( "h", ser.read(2)[0:2] )[0]
        s = ser.read(23)
        #print (mode,gps)

        roll = str(int(translate(roll,-1000,1000, 0, 35000)))
        throtal = str(int(translate(throtal,-1000,1000, 0, 35000)))
        pitch = str(int(translate(pitch,-1000,1000, 0, 35000)))
        Yaw = str(int(translate(Yaw,-1000,1000, 0, 35000)))

        mode = str(int(translate(mode,-1000,1000, 0, 35000)))
        gps = str(int(translate(gps,-1000,1000, 0, 35000)))

        return roll+","+throtal+","+pitch+","+Yaw+","+mode+","+gps

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def getData(): 
	try:
		return syinc()
	except serial.serialutil.SerialException:
		return "disconected"

def Setup(ComporT):
	strt(ComporT)