import numpy as np
import matplotlib.pyplot as plt

with open("mpstat.txt","r") as f:
    lines = f.readlines()
    usr_list = []
    sys_list = []
    idle_list = []
    for idx,line in enumerate(lines):
        columns = [column.strip() for column in line.split()]
        if len(columns) < 3:
            continue
        if columns[3] != "all":
            continue
        usr_list.append(float(columns[4]))
        sys_list.append(float(columns[6]))
        idle_list.append(float(columns[-1]))

    print(f"Average percent user time: {np.mean(usr_list)}")
    print(f"Average percent system time: {np.mean(sys_list)}")
    print(f"Average percent idle time: {np.mean(idle_list)}")