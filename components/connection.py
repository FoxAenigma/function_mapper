import serial
import re
import sys

global UART, PATTERN, MAX_ITER
try:
	UART = serial.Serial("COM3")
	PATTERN = r'sensorX:[0-9]+ sensorY:[0-9]+ !'
	MAX_ITER = 10
except:
	print("Need a microcontroller to init, please connect device")
	sys.exit(1)
	
def get_data(iteration = 0):
	if iteration > MAX_ITER:
		print("Microcontroller error")
		return {
			"sensorX": None,
			"sensorY": None,
		} 
	try:
		raw = UART.read_until(b'!').decode('ascii')
		if bool(re.search(PATTERN, raw)):
			chunk = raw.split()
			return {
				"sensorX": float(chunk[0].split(":")[-1]),
				"sensorY": float(chunk[1].split(":")[-1]),
			}
		else:
			get_data(iteration+1)
	except:
		get_data(iteration+1)
	