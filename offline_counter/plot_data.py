import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, butter, lfilter, freqz
import matplotlib.pyplot as plt
from pathlib import Path
import find_extrema

# Replicate these lines in Python console

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLING_RATE = 250 #hz

# read in file with better column names
signal = pd.read_csv(BASE_DIR / 'data' / 'samples.csv', names=['time', 'ml2', 'v5'])

# drop the bad data
signal = signal.drop([0, 1])

# set the correct types
signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})

raw = signal['v5'].to_numpy()

# Center data at zero instead of 5 or whatever it's normally at
raw = raw - raw[0]

### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_pass = np.convolve(raw, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_pass = np.convolve(low_pass, [-0.000798178, -0.003095487,-0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

# Finds diff 
diff = np.diff(band_pass)

# Squares diff
squared = diff * diff 

# Applys a moving average
weights = np.ones(38)
movingAvg = np.convolve(squared, weights)

# Finds extrema
x,y = find_extrema.find_extrema(movingAvg, SAMPLING_RATE)

# Number of heartbeats
print(f"{len(x)} heartbeats detected")

# plot the data
plt.plot(movingAvg)

plt.scatter(x, y, c='orange', s=100)
# now show the plot for real
plt.show()
