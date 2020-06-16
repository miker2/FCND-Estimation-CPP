import pandas as pd

GPS = pd.read_csv("config/log/Graph1.txt")
try:
    print(f"GPS std: {GPS[' Quad.GPS.X'].std()}")
except KeyError:
    print("Not the right file. Did you run scenario '06_NoisySensor'")

IMU = pd.read_csv("config/log/Graph2.txt")
try:
    print(f"IMU std: {IMU[' Quad.IMU.AX'].std()}")
except KeyError:
    print("Not the right file. Did you run scenario '06_NoisySensor'")
