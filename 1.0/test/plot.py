import numpy as np
from matplotlib import pyplot as plt

#plt.style.available       
#plt.style.use("ggplot") 

# data path
#data = open("R.txt","r")
data = open("delay_5ns.txt","r")
lines = data.readlines()[1:]

# 0->R; 1->delay
mode = 1

T = []
if mode == 0:
    # parameters
    HRS = []
    LRS = []

    # import data
    for line in lines:
        vector_line = line.split()
        T.append(float(vector_line[0])+273)
        HRS.append(1/float(vector_line[1]))
        LRS.append(1/float(vector_line[2]))
    data.close()

    # plot
    plt.xlabel("Temperature (K)")
    plt.ylabel("Conductance (S)")

    plt.plot(T, HRS, '-o', label="HRS")
    plt.plot(T, LRS, '--^', label="LRS")

elif mode == 1:
    tHL = []
    tLH = []
    tp = []

    for line in lines:
        vector_line = line.split()
        T.append(float(vector_line[0])+273)
        tHL.append(float(vector_line[1]))
        tLH.append(float(vector_line[2]))
        tp.append((float(vector_line[1])+float(vector_line[2]))/2)
    data.close()
    
    plt.xlabel("Temperature (K)")
    plt.ylabel("delay (ns)")
    plt.title("clk 5ns")

    plt.plot(T, tHL, '-o', label="tHL")
    plt.plot(T, tLH, '--^', label="tLH")
    plt.plot(T, tp, '-.x', label="tp")

plt.grid(linestyle='--')
plt.legend()
plt.show()
