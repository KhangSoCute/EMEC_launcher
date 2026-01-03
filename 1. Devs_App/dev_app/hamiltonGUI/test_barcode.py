import serial
import pandas as pd

ser = serial.Serial('COM4', baudrate=9600, timeout=0.2)

num_sample = int(input('Number of samples:'))
arr_barcord = []
num_cols = ["No.Sample"]

try:
    while True:
        data = ser.readline().decode('utf-8').strip()

        if data:
            arr_barcord.append(data)

except KeyboardInterrupt:
    pass

for i in range(num_sample):
    num = f"No.{i+1}"
    num_cols.append(num)

arr_barcord.insert(0, num_sample)

print(num_cols)
print(arr_barcord)

df = pd.DataFrame([num_cols,arr_barcord])

print(df)

df.to_excel("output.xls", index=False,header=False)





