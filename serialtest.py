# a program to test UART communittion with the RPI
import serial

port = serial.Serial("/dev/serial0", baudrate=9600)

while True:
#	port.write('U')
#	port.write('\r\n\nSend 7 bytes of Data:')
	rcv = port.read(1)
#	rcv = port.readline()
	print(str(rcv))
#	print('msg end\n')
#	port.write('\r\nYou sent: ' + repr(rcv))
