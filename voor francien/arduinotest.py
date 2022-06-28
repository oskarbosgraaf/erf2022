import serial
import time

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('/dev/ttyACM0', 9800, timeout=1)
time.sleep(2)

for i in range(50):
    line = ser.readline()   # read a byte
    if line:
        data = [int(word) for word in line.split() if word.isdigit()]
        print(data)
ser.close()