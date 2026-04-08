import serial
import time
import pandas as pd

# load synthetic EMG data
data = pd.read_csv("synthetic_emg.csv")

ser = serial.Serial('COM3', 9600, timeout=1)   # change COM port
time.sleep(2)

system_state = "STANDBY"
index = 0

print("Listening...")

while True:

    # read button command
    msg = ser.readline().decode(errors='ignore').strip()

    if msg:

        print("Received:", msg)

        if msg == "START":
            system_state = "RUNNING"
            print("Streaming EMG data...")

        elif msg == "STOP":
            system_state = "STOPPED"
            print("Stopped")

        elif msg == "STANDBY":
            system_state = "STANDBY"
            print("Standby mode")

        elif msg == "RESET":
            system_state = "STANDBY"
            index = 0
            print("Reset dataset index")

    # simulate real-time EMG stream
    if system_state == "RUNNING":

        if index < len(data):

            row = data.iloc[index]

            print("EMG sample:", row.values)

            # here later we feed into LSTM

            index += 1

            time.sleep(0.05)   # controls speed

        else:
            print("End of dataset")
            system_state = "STANDBY"