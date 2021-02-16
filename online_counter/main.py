import sys
from plot_data import DataVis
from live_data_simulator import DataSimulator
import multiprocessing as mp

SAMPLING_RATE = 250 #hz


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("usage: main.py (filename)")
        sys.exit(1)

    # Queue to use between data simulator and grapher
    q = mp.Queue()
    
    data_sim = DataSimulator(sys.argv[1])

    # Starts async process of appending "live" data to queue
    p1 = mp.Process(target=data_sim.start, args=(q, SAMPLING_RATE))
    p1.start()

    # Plots data from queue based on sample rate given
    data_vis = DataVis(q, SAMPLING_RATE)
    data_vis.start()

    # Terminates and joins async process back
    p1.terminate()
    p1.join()
