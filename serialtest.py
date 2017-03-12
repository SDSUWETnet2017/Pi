# a program to test UART communittion with the RPI
import serial

port = serial.Serial("/dev/serial0", baudrate=115200)

while True:
#	port.write('U')
	port.write('\r\n\nSend 7 bytes of Data:')
	rcv = port.read(7)
	print(str(rcv))
	port.write('\r\nYou sent: ' + repr(rcv))
