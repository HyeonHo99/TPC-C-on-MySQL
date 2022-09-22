import numpy as np
import matplotlib.pyplot as plt

indexes = range(27,147)
x_index = [i*10 for i in range(1,121)]
y_index = []

for i in range(1,6):
    with open(f"./{i*10}p/tpcc-result.txt","r") as f:
        lines = f.readlines()
        lines = [lines[i] for i in indexes]
        trx_list = []

        for line in lines:
            columns = [column.strip() for column in line.split(",")]
            trx_list.append(int(columns[1].replace("trx:", "").strip()))
        print(f"Buffer Size {i*10}% >> Average of trx: {np.mean(trx_list)}")
        y_index.append(trx_list)


plt.figure()
for i in range(0,5):
    plt.plot(x_index,y_index[i],label=f"{10*(i+1)}%")
    plt.legend()
    plt.xlabel('Time (10 seconds)')
    plt.ylabel('Number of transactions')
plt.savefig("trx_graph.png")
plt.show()

