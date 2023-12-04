import serial, time


arduino = serial.Serial('COM3', 9600)

def encender():
    print("Inicia +")
    arduino.write(b'1')
    time.sleep(1)
    print("Finaliza +")

def apagar():
    print("Inicia -")
    arduino.write(b'0')
    time.sleep(1)
    print("Finaliza -")

time.sleep(2)
encender()
time.sleep(10)
apagar()
time.sleep(10)

arduino.close()