import numpy as np
import matplotlib.pyplot as plt

for i in range(1,6):
    with open(f"./{i*10}p/iostat.txt","r") as f:
        lines = f.readlines()
        lines = [line for line in lines if "sda" in line]
        r_list = []
        w_list = []
        for line in lines:
            columns = [column.strip() for column in line.split()]
            r_list.append(float(columns[1]))
            w_list.append(float(columns[7]))

        avg_read = np.mean(r_list)
        avg_write = np.mean(w_list)

        print(f"Buffer Size {i*10}%")
        print(f"Average r/s: {avg_read}")
        print(f"Average w/s: {avg_write}")
        print(f"Read/Write ratio: {(avg_read / (avg_read + avg_write)) * 100}:{(avg_write / (avg_read + avg_write)) * 100}\n")
