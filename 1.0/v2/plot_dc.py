import numpy as np
import matplotlib.pyplot as plt

# file path
file = './without_variation/'

# load file
IV_25C = np.load(file+'25C.npy',allow_pickle=True).item()
IV_50C = np.load(file+'50C.npy',allow_pickle=True).item()
IV_75C = np.load(file+'75C.npy',allow_pickle=True).item()
IV_100C = np.load(file+'100C.npy',allow_pickle=True).item()
IV_125C = np.load(file+'125C.npy',allow_pickle=True).item()

dataset = [IV_25C, IV_50C, IV_75C, IV_100C, IV_125C]

# print resistance
def var_name(var,all_var=locals()):
    return [var_name for var_name in all_var if all_var[var_name] is var][0]

for data in dataset:
    print(var_name(data)+":")
    tmp = [abs(i-0.1) for i in data['V'][:int(len(data['0V'])/4)]]
    x = tmp.index(min(tmp))
    print(str(x)+': '+str(data['I'][x])+' A')
    tmp = [abs(i-0.1) for i in data['V'][:int(len(data['V'])/2)]]
    x = tmp.index(min(tmp))
    print(str(x)+': '+str(data['I'][x])+' A')

# plot settings
plt.rcParams['font.sans-serif'] = "Arial"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.size'] = 10.
f, ax = plt.subplots(2, 1)
f.set_size_inches(8., 7.)

# plot
ax[0].semilogy(IV_25C['V'], IV_25C['I'], label='25C')
ax[0].semilogy(IV_50C['V'], IV_50C['I'], label='50C')
ax[0].semilogy(IV_75C['V'], IV_75C['I'], label='75C')
ax[0].semilogy(IV_100C['V'], IV_100C['I'], label='100C')
ax[0].semilogy(IV_125C['V'], IV_125C['I'], label='125C')
#ax[0].semilogy(IV_25C['V'][x], IV_25C['I'][x], "or")
ax[0].set_xlabel("Voltage (V)")
ax[0].set_ylabel("I (A)")
ax[0].legend()

ax[1].plot(IV_25C['V'], IV_25C['I'], label='25C')
ax[1].plot(IV_50C['V'], IV_50C['I'], label='50C')
ax[1].plot(IV_75C['V'], IV_75C['I'], label='75C')
ax[1].plot(IV_100C['V'], IV_100C['I'], label='100C')
ax[1].plot(IV_125C['V'], IV_125C['I'], label='125C')
ax[1].set_xlabel("Voltage (V)")
ax[1].set_ylabel("I (A)")
ax[1].legend()

plt.show()
