#SET/RESET
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from rram import rram

####################################
r = rram(x0=3e-9, w0=0.5e-9)

t_ramp = 1e-6
dt = 1e-10
vdd = 2

Vs1 = np.concatenate((np.linspace(0., vdd, int(t_ramp/dt)), np.linspace(vdd, vdd, int(t_ramp/dt)), np.linspace(vdd, 0., int(t_ramp/dt))))
steps = np.shape(Vs1)[0] 
Is1 = []

for v in Vs1:
    i = r.step(v, dt)
    Is1.append(i)

####################################
r = rram(x0=3e-10, w0=5e-9)

Vs2 = np.concatenate((np.linspace(0., -vdd, int(t_ramp/dt)), np.linspace(-vdd, -vdd, int(t_ramp/dt)), np.linspace(-vdd, 0., int(t_ramp/dt))))
steps = np.shape(Vs2)[0] 
Is2 = []

for v in Vs2:
    i = r.step(v, dt)
    Is2.append(i)

Is2 = np.array(Is2) * -1.

####################################
Ts = np.linspace(0., 2*steps*dt, 2*steps)
Vs = np.concatenate((Vs1, Vs2))
Is = np.concatenate((Is1, Is2))

####################################
results = {'V': Vs, 'I':Is}
np.save('25C', results)

plt.subplot(3, 1, 1)
plt.plot(Ts, Vs)
    
plt.subplot(3, 1, 2)
plt.plot(Ts, Is)

plt.subplot(3, 1, 3)
plt.semilogy(Vs, Is)

plt.show()
