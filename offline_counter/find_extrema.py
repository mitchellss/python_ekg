from scipy.signal import argrelextrema
import numpy as np
import pandas as pd
import math

HEART_MIN_REFACTORY_PERIOD = 250 # milliseconds
QRS_WINDOW = 150 # milliseconds
MS_PER_S = 1000 # milliseconds


def find_extrema(data_array, sampling_rate):
    MIN_HEIGHT = max(data_array) / 10 # Peaks must be higher than 1/10th the highest point to be considered 
    MIN_SPACING = math.ceil((sampling_rate / MS_PER_S) * HEART_MIN_REFACTORY_PERIOD) # Samples must be 250ms apart minimally
    ORDER = math.ceil(sampling_rate * QRS_WINDOW / MS_PER_S) # Samples in longest possible QRS

    # Find relative extrema on the dataset (points that are higher than n points to their left and right)
    data_peaks = argrelextrema(data_array, np.greater_equal, order=ORDER)[0]

    data_peaks_filter = data_array[data_peaks] > MIN_HEIGHT

    above_data_peaks = data_peaks[data_peaks_filter]

    x = []
    y = []

    for i in range(0, len(above_data_peaks)):

        # If not the last data point
        if i != len(above_data_peaks) - 1:

            #print(f"{above_data_peaks[i+1]} - {above_data_peaks[i]} = {above_data_peaks[i+1] - above_data_peaks[i]}")

            # Only include point if it's at least MIN_SPACING points away from last peak
            # This avoids heartbeats with small plateaus at the top being marked twice
            if above_data_peaks[i+1] - above_data_peaks[i] > MIN_SPACING:
                x.append(above_data_peaks[i]) 
                y.append(data_array[above_data_peaks[i]])

        # Mark the last point normally
        else:
            x.append(above_data_peaks[i])
            y.append(data_array[above_data_peaks[i]])

    return x, y
