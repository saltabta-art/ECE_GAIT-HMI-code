import pandas as pd
import time

csv_file = "synthetic_emg.csv"

df = pd.read_csv(csv_file)

print("Columns in file:")
print(df.columns.tolist())
print()

# Channel mapping from your CSV
time_col = "time"
calf_col = "gaslat_r_emg"
quad_col = "recfem_r_emg"
thigh_col = "bifemlh_r_emg"

print("First 5 rows:")
print(df[[time_col, calf_col, quad_col, thigh_col]].head())
print()

for i, row in df.iterrows():
    t = row[time_col]
    calf = row[calf_col]
    quad = row[quad_col]
    thigh = row[thigh_col]

    print(f"Time: {t:.3f} s")
    print(f"Calf:  {calf:.4f}")
    print(f"Quad:  {quad:.4f}")
    print(f"Thigh: {thigh:.4f}")
    print("-" * 30)

    time.sleep(0.05)   # adjust speed as needed