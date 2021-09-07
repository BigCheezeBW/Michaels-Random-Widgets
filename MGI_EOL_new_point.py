# This tool imports a bunch of selected MGI EOL snapshots and uses only the last data point (called newpoint in the snapshot), and does basic Stat analysis and plots histograms with 3sigma lines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def load_function():

    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #Data columns to be imported
    cols=["DUT Avg Velocity (RPM)",
          "DUT Avg Calculated Torque (Nm)",
          "ICM2 - Ud (V)",
          "ICM2 - Uq (V)",
          "ICM2 - Id (A)",
          "ICM2 - Iq (A)",
          "DUT2 Temp (Deg C)"]

    skippedrows = list(np.arange(2,22,1))


    #for loop load the data
    dataList=[]
    loadTime=0
    for name in fileNames:
        print("Loading new file: "+name)
        t0=t.time()
        data=pd.read_csv(name,usecols=cols,index_col=False,header = 1,skiprows=skippedrows)
        dataList.append(data)
        t1=t.time()
        deltaT=t1-t0
        loadTime=loadTime+deltaT
    print("Finished loading files, total load time: "+str(round(loadTime,3))+" seconds")


    #Mesh all of the dataframes from dataList together into one dataFrame
    finalFrame=pd.concat(dataList,ignore_index=True)
    print_full(finalFrame)
    #Return dataframe and used columns
    return finalFrame,cols,fileNames

def main():
    finalFrame,cols,fileNames = load_function()
    # This does calculates the |Vdq| amplitude for each unit and makes in a new column called ICM2 - Udq (V)
    finalFrame['ICM2 - Udq (V)'] = (finalFrame["ICM2 - Ud (V)"] ** 2 + finalFrame["ICM2 - Uq (V)"] ** 2) ** 0.5
    cols.append("ICM2 - Udq (V)")
    std = finalFrame.std(axis = 0, skipna = True)
    mean = finalFrame.mean(axis = 0, skipna = True)
    num = 0
    # This prints each datum as a hhistogram of units, IDK how to make all graphs pop up together
    for col in cols:
        plt.figure(num)
        plt.hist(finalFrame[col],15,color='g')
        plt.axvline(x=(mean[col]-3*std[col]),color='r')
        plt.axvline(x=(mean[col]+3*std[col]),color='r')
        plt.xlabel(col)
        plt.ylabel('Count')
        plt.title('Histogram of EOL')
        plt.show()
        num+=1

main()
