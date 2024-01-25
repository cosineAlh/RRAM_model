import numpy as np
import matplotlib.pyplot as plt

# file path
file = ''#'./set_reset/'
config = 'RESET'

# load file
R_25C = np.load(file+config+'_25C.npy',allow_pickle=True).item()
R_50C = np.load(file+config+'_50C.npy',allow_pickle=True).item()
R_75C = np.load(file+config+'_75C.npy',allow_pickle=True).item()
R_100C = np.load(file+config+'_100C.npy',allow_pickle=True).item()
R_125C = np.load(file+config+'_125C.npy',allow_pickle=True).item()

dataset = [R_25C, R_50C, R_75C, R_100C, R_125C]

# print delay
def var_name(var,all_var=locals()):
    return [var_name for var_name in all_var if all_var[var_name] is var][0]

print(config)
for data in dataset:
    half = (data['R'][-1] + data['R'][0])/2
    t = [abs(i-half) for i in data['R']].index(min([abs(i-half) for i in data['R']]))
    print(var_name(data)+": "+str(round(data['t'][t]/1e-9, 4))+" ns")

# plot settings
f, ax = plt.subplots(2, 1)
f.set_size_inches(8., 7.)
f.suptitle(config)

# plot
ax[0].plot(R_25C['t'], R_25C['V'])
ax[0].set_xlabel("time (s)")
ax[0].set_ylabel("pulse (V)")

ax[1].plot(R_25C['t'], R_25C['R'], label='25C')
ax[1].plot(R_50C['t'], R_50C['R'], label='50C')
ax[1].plot(R_75C['t'], R_75C['R'], label='75C')
ax[1].plot(R_100C['t'], R_100C['R'], label='100C')
ax[1].plot(R_125C['t'], R_125C['R'], label='125C')
ax[1].set_xlabel("time (s)")
ax[1].set_ylabel("R ($\Omega$)")
ax[1].legend()

plt.show()
