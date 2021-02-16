# python_ekg
Online and offline data processing of EKG data for the counting of heartbeats

This project was created for an engineering elective course. It utilizes data from https://physionet.org

The offline counter takes entire csv files of EKG data and counts the heartbeats that occur based on a number of conditions.

The online counter loads csv files into its own process and feeds it to the heartbeat counter in order to simulate real-time data.

Example Usage: `python online_counter/main.py data/mitdb_201.csv`
