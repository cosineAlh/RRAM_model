#SET/RESET
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import argparse
from rram import rram

t_ramp = 1e-6
dt = 1e-10

############################
parser = argparse.ArgumentParser()
#parser.add_argument('--gap_min', type=float, default=2e-10)
#parser.add_argument('--gap_max', type=float, default=14e-10)
parser.add_argument('--T_ini', type=float, default=100)
args = parser.parse_args()
#print (args)

LUT  = {'25':(2e-10, 14e-10), '50':(2.1e-10, 13.9e-10), '75':(2.3e-10, 13.7e-10), '100':(2.5e-10, 13.5e-10), '125':(2.6e-10, 13.4e-10)}
gap_min = LUT[str(int(args.T_ini))][0]
gap_max = LUT[str(int(args.T_ini))][1]
T_ini = args.T_ini + 273
deltaGap0 = 0.1
model_switch = 0

#############SET############
r = rram(shape=(1, 1), gap_min=gap_min, gap_max=gap_max, gap_ini=gap_max, T_ini = T_ini, deltaGap0=deltaGap0, model_switch=model_switch)

vdd = 2

Vs = np.concatenate((np.linspace(0, vdd, int(t_ramp/dt)), np.linspace(vdd, vdd, int(1e-6/dt)), np.linspace(vdd, 0, int(t_ramp/dt))))
steps = np.shape(Vs)[0] 
Is = []
Rs = []
Temp = []

for v in Vs:
    Rs.append(r.R()[0][0])
    i, Temp_ = r.step(np.reshape(v, (1, 1)), dt)
    Is.append(i[0][0])
    Temp.append(Temp_[0][0])
    
Vs1 = np.copy(Vs)
Is1 = np.copy(Is)
Rs1 = np.copy(Rs)
Temp1 = np.copy(Temp)

############RESET###########
#r = rram(shape=(1, 1), gap_min=gap_min, gap_max=gap_max, gap_ini=gap_min, deltaGap0=deltaGap0, model_switch=model_switch)

vdd = 2

Vs = np.concatenate((np.linspace(0, -vdd, int(t_ramp/dt)), np.linspace(-vdd, -vdd, int(1e-6/dt)), np.linspace(-vdd, 0, int(t_ramp/dt))))
steps = np.shape(Vs)[0] 
Is = []
Rs = []
Temp = []

for v in Vs:
    Rs.append(r.R()[0][0])
    i, Temp_ = r.step(np.reshape(v, (1, 1)), dt)
    Is.append(i[0][0])
    Temp.append(Temp_[0][0])
  
Is = np.array(Is) * -1.

Vs2 = np.copy(Vs)
Is2 = np.copy(Is)
Rs2 = np.copy(Rs)
Temp2 = np.copy(Temp)

############################
Ts = np.linspace(0., 2*steps*dt, 2*steps)
Vs = np.concatenate((Vs1, Vs2))
Is = np.concatenate((Is1, Is2))
Rs = np.concatenate((Rs1, Rs2))
Temp = np.concatenate((Temp1, Temp2))

############################
ratio = np.max(Rs) / np.min(Rs)

flag = True
flag = flag and (ratio > 90.) and (ratio < 150.)
#print (np.min(Rs) / 1e6, np.max(Rs) / 1e6, ratio)
flag = True

if flag:
    results = {'V': Vs, 'I':Is, 'T':Temp, 't':Ts}
    #np.save(str(int(T_ini-273))+'C', results)

    #plt.rcParams['font.sans-serif'] = "Arial"
    #plt.rcParams['font.family'] = "sans-serif"
    #plt.rcParams['font.size'] = 10.
    f, ax = plt.subplots(3, 1)
    #f.set_size_inches(3.5, 3.5)

    ax[0].semilogy(Vs, Is)
    ax[1].semilogy(Ts, Rs)
    ax[2].plot(Ts, Temp)

    #name = '%0.12f_%0.12f.png' % (args.gap_min, args.gap_max)
    plt.show()
