import pandas as pd
import serial
import time

csv_file = "synthetic_emg.csv"
port = "COM4"   # change this to your Arduino port
baud = 9600

df = pd.read_csv(csv_file)

time_col = "time"
calf_col = "gaslat_r_emg"
quad_col = "recfem_r_emg"
thigh_col = "bifemlh_r_emg"

activities = ["Turn Left", "Turn Right", "Step Up/Down", "Straight"]

ser = serial.Serial(port, baud, timeout=0.1)
time.sleep(2)

running = False
index_val = 0
start_time = 0

print("Listening...")

while True:
    msg = ser.readline().decode(errors="ignore").strip()

    if msg:
        print("Received:", msg)

        if msg == "START":
            running = True
            start_time = time.time()
            print("Status: WALKING")

        elif msg == "STOP":
            running = False
            print("Status: STOPPED")

        elif msg == "STANDBY":
            running = False
            print("Status: STANDBY")

        elif msg == "RESET":
            running = False
            index_val = 0
            print("Status: READY")
            print("Time: 00:00")
            print("Activity: Ready")
            print("Calf: 0.00")
            print("Quad: 0.00")
            print("Thigh: 0.00")
            print("Progress: 0%")

    if running:
        if index_val < len(df):
            row = df.iloc[index_val]

            elapsed = int(time.time() - start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60

            calf = row[calf_col]
            quad = row[quad_col]
            thigh = row[thigh_col]
            activity = activities[(index_val // max(1, len(df)//4)) % 4]
            progress = int(((index_val + 1) / len(df)) * 100)

            print(f"Time: {minutes:02d}:{seconds:02d}")
            print(f"Activity: {activity}")
            print(f"Calf: {calf:.4f}")
            print(f"Quad: {quad:.4f}")
            print(f"Thigh: {thigh:.4f}")
            print(f"Progress: {progress}%")
            print("-" * 30)

            index_val += 1
            time.sleep(0.05)
        else:
            running = False
            print("End of dataset")
            print("Status: READY")