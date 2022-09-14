import numpy as np
import matplotlib.pyplot as plt

with open("tpcc-result.txt","r") as f:
    lines = f.readlines()
    indexes = range(27,147)
    sec_list = []
    trx_list = []
    res95_list = []
    res99_list = []
    max_rt_list = []
    for i,line in enumerate(lines):
        if i not in indexes:
            continue
        columns = [column.strip() for column in line.split(",")]
        sec_list.append(int(columns[0]))
        trx_list.append(int(columns[1].replace("trx:","").strip()))
        res95_list.append(float(columns[2].replace("95%:","").strip()))
        res99_list.append(float(columns[3].replace("99%:", "").strip()))
        max_rt_list.append(float(columns[4].replace("max_rt:", "").strip()))

    print(f"Average of trx: {np.mean(trx_list)}")
    print(f"Average of 95%: {np.mean(res95_list)}")
    print(f"Average of 99%: {np.mean(res99_list)}")
    print(f"Average of max_rt: {np.mean(max_rt_list)}")

    # plt.figure()
    # plt.plot(sec_list,trx_list,label="trx")
    # plt.legend()
    # plt.xlabel('Time (10 seconds)')
    # plt.ylabel('Number of transactions')
    # plt.savefig("trx_graph.png")
    # plt.show()

    plt.figure()
    plt.plot(sec_list, res95_list, label="95%")
    plt.plot(sec_list, res99_list, label="99%")
    plt.plot(sec_list, max_rt_list, label="maximum")
    plt.legend()
    plt.xlabel('Time (10 seconds)')
    plt.ylabel("Response time (second)")
    plt.savefig("rt_graph.png")
    plt.show()
