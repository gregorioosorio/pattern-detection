## Written and copyright by Mohit Agarwal
## Georgia Institute of Technology
## Email: magarwal37@gatech.edu

import os
import numpy as np
from scipy.signal import *
import csv
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft

#Options to read: 'EEG-IO', 'EEG-VV', 'EEG-VR', 'EEG-MB'
data_folder = 'EEG-IO' 

# Parameters and bandpass filtering
fs = 128
def lowpass(sig, fc, fs, butter_filt_order):
    B,A = butter(butter_filt_order, np.array(fc)/(fs/2), btype='low')
    return lfilter(B, A, sig, axis=0)

# function to read stimulations
def decode_stim(data_path, file_stim):
    interval_corrupt = []
    blinks = []
    n_corrupt = 0
    with open(os.path.join(data_path,file_stim)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0]=="corrupt":
                n_corrupt = int(row[1])
            elif n_corrupt > 0:
                if float(row[1]) == -1:
                    t_end = data_sig[-1,0]
                else:
                    t_end = float(row[1])
                interval_corrupt.append([float(row[0]), t_end])
                n_corrupt = n_corrupt - 1
            elif row[0]=="blinks":
                #check that n_corrupt is 0
                if not n_corrupt==0:
                    print ("!Error in parsing")
            else:
                blinks.append([float(row[0]), int(row[1])])
    blinks = np.array(blinks)

    return interval_corrupt, blinks 

# Reading data files
file_idx = 0
list_of_files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f)) and '_data' in f]
file_sig = list_of_files[file_idx]
file_stim = list_of_files[file_idx].replace('_data','_labels')
print ("Reading: ", file_sig, file_stim)

# Loading data
if data_folder == 'EEG-IO' or data_folder == 'EEG-MB':
	data_sig = np.loadtxt(open(os.path.join(data_folder,file_sig), "rb"), delimiter=";", skiprows=1, usecols=(0,1,2))
elif data_folder == 'EEG-VR' or data_folder == 'EEG-VV':
	data_sig = np.loadtxt(open(os.path.join(data_folder,file_sig), "rb"), delimiter=",", skiprows=5, usecols=(0,1,2))
	data_sig = data_sig[0:(int(200*fs)+1),:]
	data_sig = data_sig[:,0:3]
	data_sig[:,0] = np.array(range(0,len(data_sig)))/fs

# Loading Stimulations
interval_corrupt, groundtruth_blinks = decode_stim(data_folder, file_stim)

sr = 128
X = fft(data_sig[:,1])
N = len(X)
n = np.arange(N)
T = N/sr
freq = n/T

ts = 1.0/sr
t = np.arange(0,1,ts)

plt.figure(figsize = (12, 6))
plt.subplot(121)


plt.stem(freq, np.abs(X), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')

plt.subplot(122)
plt.plot(data_sig[:,0], ifft(X), 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()

plt.show()