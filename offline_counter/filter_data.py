import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import find_extrema

##### Replicate these lines in Python console

# read in file with better column names
signal = pd.read_csv('samples.csv', names=['time', 'ml2', 'v5'])

# drop the bad data in rows 0 and 1
signal = signal.drop([0, 1])

# set the correct types
signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})

#pull out the V5 signal
v5 = signal['v5'].to_numpy()

plt.plot(v5)
plt.title('Signal')
plt.show()

### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_pass = np.convolve(v5, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_pass = np.convolve(low_pass, [-0.000798178, -0.003095487,-0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

plt.plot(band_pass)
plt.title('Filtered')
plt.show()

### pass data through weighter differiator
diff = np.convolve(band_pass,[1,2,-2,-1])   #I think this is incorrect as it does not look "forward" but should work

# plt.plot(band_pass)
# plt.title('Diffed')
# plt.show()


## pass data through square function
squared = diff * diff

#plt.plot(squared)
#plt.title('Squared')
#plt.show()

## pass through moving average of 150ms window @ 250 Hz => 38 samples
weights = np.ones(38)
average = np.convolve(squared, weights)

plt.plot(average)
x, y = find_extrema.find_extrema(average)
print(len(x))

plt.scatter(x,y,c='orange',s=100)
plt.title('Averaged')
plt.show()
