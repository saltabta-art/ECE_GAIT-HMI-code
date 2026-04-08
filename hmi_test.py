import serial
import time

ser = serial.Serial('COM3', 9600, timeout=1) # change COM3 or COM4 to your port
time.sleep(2)

system_running = False

print("Listening...")

while True:
    msg = ser.readline().decode(errors='ignore').strip()

    if msg:
        print("Received:", msg)

        if msg == "START":
            system_running = True
            print("Walking mode started")

        elif msg == "STOP":
            system_running = False
            print("Walking mode stopped")