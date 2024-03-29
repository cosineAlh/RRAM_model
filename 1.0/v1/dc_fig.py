import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from rram_test import rram

############################
r = rram(shape=(2, 2), gap_ini=19e-10)

dt = 1e-7
Vs = np.concatenate((np.linspace(0., 2., int(4e-3/dt)), np.linspace(2., 2., int(1e-6/dt)), np.linspace(2., 0., int(4e-3/dt))))
steps = np.shape(Vs)[0] 
Ts = np.linspace(0., steps*dt, steps)
Is = []

for v in Vs:
    i = r.step(v, dt)
    Is.append(i)

Vs1 = np.copy(Vs)
Is1 = np.copy(Is)

############################
r = rram(shape=(2, 2), gap_ini=2e-10)

dt = 1e-7
Vs = np.concatenate((np.linspace(0., -2., int(4e-3/dt)), np.linspace(-2., -2., int(1e-6/dt)), np.linspace(-2., 0., int(4e-3/dt))))
steps = np.shape(Vs)[0] 
Ts = np.linspace(0., steps*dt, steps)
Is = []

for v in Vs:
    i = r.step(v, dt)
    Is.append(i)
  
Is = np.array(Is) * -1.

Vs2 = np.copy(Vs)
Is2 = np.copy(Is)

############################
Ts = np.linspace(0., 2*steps*dt, 2*steps)
Vs = np.concatenate((Vs1, Vs2))
Is = np.concatenate((Is1, Is2))
  
############################
plt.rcParams['font.sans-serif'] = "Arial"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.size'] = 10.
f, ax = plt.subplots()
f.set_size_inches(3.5, 3.5)

ax.semilogy(Vs, Is)

plt.savefig('memristor_dc_.png', dpi=1000, bbox_inches='tight')
