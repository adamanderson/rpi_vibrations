from scipy.signal import periodogram, welch
from python_mma8451.read_accelerometer import read_file, read_for_time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import argparse as ap

P = ap.ArgumentParser(description='Quick plotting of accelerometer data for '
                      'diagnostic purposes.',
                      formatter_class=ap.ArgumentDefaultsHelpFormatter)
P.add_argument('filename', help='Name of data file to read.')
P.add_argument('--duration', type=float, default=1000,
               help='Duration (in seconds) of data chunks to plot.')
args = P.parse_args()

data, times, rate = read_file(args.filename)
axes = ['x', 'y', 'z']

tmin = times[0]
jfig = 0
while tmin < times[-1]:
    for jaxis in range(3):
        plt.figure()
        datarange = (times > tmin) & (times < tmin+args.duration)
        f, psd = periodogram(data[datarange, jaxis], fs=rate, window='hanning')
        plt.subplot(2,1,1)
        plt.plot(times[datarange], data[datarange, jaxis], linewidth=0.5)
        plt.xlim([np.min(times[datarange]), np.max(times[datarange])])
        plt.xlabel('time [sec]')
        plt.ylabel('acceleration [g]')
        plt.title('{} axis, chunk {}'.format(axes[jaxis], jfig)) 
        plt.subplot(2,1,2)
        plt.semilogy(f, np.sqrt(psd), linewidth=0.5)
        plt.xlim([0, 100])
        plt.xlabel('frequency [Hz]')
        plt.ylabel('acceleration ASD [g / rtHz]')
        plt.tight_layout()
        plt.savefig('{}_axis_data_fig{}.png'.format(axes[jaxis], jfig), dpi=200)
        plt.close()
    tmin = tmin + args.duration
    jfig += 1
