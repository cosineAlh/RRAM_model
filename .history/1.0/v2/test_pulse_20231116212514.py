import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import argparse
from rram import rram

############################
parser = argparse.ArgumentParser()
#parser.add_argument('--gap_min', type=float, default=2e-10)
#parser.add_argument('--gap_max', type=float, default=14e-10)
parser.add_argument('--T_ini', type=float, default=25)
args = parser.parse_args()

LUT  = {'25':(2e-10, 14e-10), '50':(2.1e-10, 13.9e-10), '75':(2.3e-10, 13.7e-10), '100':(2.5e-10, 13.5e-10), '125':(2.6e-10, 13.4e-10)}
gap_min = LUT[str(int(args.T_ini))][0]
gap_max = LUT[str(int(args.T_ini))][1]
T_ini = args.T_ini + 273
deltaGap0 = 0.1
model_switch = 1

#############PULSE############
r = rram(shape=(1, 1), gap_min=gap_min, gap_max=gap_max, gap_ini=gap_min, T_ini = T_ini, deltaGap0=deltaGap0, model_switch=model_switch)

T = 5e-9
dt = 1e-12
pulse_width = 2.5e-9
steps = int(T/dt) + 1
Ts = np.linspace(0., T, steps)
Vdd = -2

Vs = ((signal.square(2*np.pi*(1./(2*pulse_width))*Ts, duty=0.5)+1.)/2.)*Vdd
Is = []
Rs = []

#T2 = 5e-9
Ts2 = np.linspace(0., T2, steps)

for v in Vs:
    Rs.append(r.R()[0][0])
    i, _ = r.step(np.reshape(v, (1, 1)), dt)
    Is.append(-i[0][0])
  
############################################################
results = {'V': Vs, 'I':Is, 'R':Rs, 't':Ts}
np.save('RESET_'+str(int(T_ini-273))+'C', results)

f, ax = plt.subplots(2, 1)
#f.set_size_inches(3.5, 4.)

ax[0].plot(Ts, Vs)
ax[0].set_xlabel("time (s)")
ax[0].set_ylabel("Voltage (V)")

ax[1].plot(Ts, Rs)
ax[1].set_xlabel("time (s)")
ax[1].set_ylabel("Resistance ($\Omega$)")
plt.show()
#plt.savefig('test.png', dpi=1000, bbox_inches='tight')
