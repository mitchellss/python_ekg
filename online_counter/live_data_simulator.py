import time
from pathlib import Path
import pandas as pd

class DataSimulator():
    def __init__(self, filename):
        #BASE_DIR = Path(__file__).resolve().parent.parent
        signal = pd.read_csv(filename, names=['time', 'ml2', 'v5'], dtype='unicode')
        # drop the bad data
        signal = signal.drop([0, 1])
        # set the correct types
        signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})
        self.raw = [signal['v5'].iloc[0]] * 500 + signal['v5'].tolist() + [signal['v5'].iloc[0]] * 2000

    def start(self, queue, sampling_rate):
        """
        Feed data into queue.

        For whatever reason putting ANY timer ( time.sleep(0.00001) ) on
        this class makes it run SUPER slow. Just fill up the queue completely
        and then use the timer on the .get() side
        """
        count = 0
        for i in self.raw:
            queue.put(i)
            count += 1

if __name__ == "__main__":
    sim = DataSimulator('samples.csv')
