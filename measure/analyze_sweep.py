import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import periodogram
from scipy.integrate import quad
from scipy.interpolate import interp1d
import pickle
from python_mma8451 import read_accelerometer 
import argparse as ap
import os.path

def motor_freq(voltage):
    '''
    Calibration of motor frequency as a function of applied voltage.

    Parameters
    ----------
    voltage : float
        Voltage of motors.
    
    Returns
    -------
    freq : float
        Frequency of motor.
    '''
    return 33.96 * (voltage**0.44) - 24.14


def find_psd_peaks(data, fs, freq_range=None, averaging=False, plot=False,
                   plot_filename='psd_peak.png'):
    '''
    Calculate the PSD of data at peaks in the PSD. Several schemes for doing
    this are available, as specified by the function arguments.

    Parameters
    ----------
    data : arr
        Time-ordered data whose PSD is to be calculated.
    fs : float
        Sampling rate of argument `data`
    freq_range : float, list of 2 elements, or None
        Frequency or range at which to get power in PSD. If a single float,
        then function returns the value of the PSD at that frequency, with
        linear interpolation between the closest frequency bins. If a list of
        two elements, then the first and second elements are the lower and
        upper points of the frequency range to analyze. If `None`, then take
        the maximum of the PSD over the entire frequency range.
    averaging : bool
        If `freq` argument is a list of two elements, then compute the PSD
        return value by taking the average power between the endpoints.
    plot : bool
        Save plot of PSD with peak locations indicated.
    plot_filename : str
        Filename of figure to save.

    Returns
    -------
    freq_peak : float or list of 2 elements
        If the peak PSD is computed at a single frequency, then return a single
        number which is that frequency. If the peak PSD is computed over a
        range of frequencies, then return a list of 2 elements containing the
        lower and upper elements of the frequency range.
    psd_peak : float
        PSD of data, calculated according to the scheme specified by arguments
        `freq` and `averaging`.
    '''
    freq, psd = periodogram(data, fs, return_onesided=True, window='hanning')

    finterp = interp1d(freq, psd)

    if freq_range is None:
        indmax = np.argmax(psd)
        freq_peak = freq[indmax]
        psd_peak = psd[indmax]
    elif type(freq_range) is list:
        ind_freq_range = (freq > freq_range[0]) & (freq < freq_range[1])
        if averaging == False:
            indmax = np.argmax(psd[ind_freq_range])
            freq_peak = freq[ind_freq_range][indmax]
            psd_peak = psd[ind_freq_range][indmax]
        else:
            freq_peak = freq_range
            psd_peak = quad(finterp, freq_range[0], freq_range[1])
    elif type(freq_range) is float:
        freq_peak = freq_range
        psd_peak = finterp(freq_range)

    if plot:
        plt.figure()
        print('plotting...')
        plt.semilogy(freq, psd, linewidth=0.5)
        yl = plt.gca().get_ylim()
        plt.plot([freq_peak, freq_peak], yl, 'r--', linewidth=0.5)
        plt.savefig(plot_filename, dpi=150)
        print(plot_filename)
        plt.close()
    
    return freq_peak, psd_peak


def analyze_psds(hk_filename, data_path=None, psd_plots=False,
                motor_cal_func=motor_freq):
    '''
    Parameters
    ----------
    hk_filename : str
        Name of housekeeping data file to read.
    data_path : str
        Name of alternate path to data file. Use this, for example, if data
        have been copied off the raspberry pi and are being analyzed on another
        machine.
    psd_plots : bool
        Generate plots of individual PSDs.
    motor_cal_func : function
        Function returning the frequency of a motor as a function of the
        applied voltage.

    Returns
    -------
    psd_data : dict
        Dictionary of peaks in the PSDs and their frequencies from the motor
        sweep data.
    '''
    with open(hk_filename, 'rb') as f:
        hk_data = pickle.load(f)

    axes = ['x', 'y', 'z']

    psd_data = dict()
    for motor_value in hk_data:
        psd_data[motor_value] = dict()

        if data_path is None:
            acc_filename = psd_data[motor_value]['file']
        else:
            print(hk_data[motor_value])
            old_filename = hk_data[motor_value]['file']
            acc_filename = os.path.join(data_path, os.path.basename(old_filename))

        acc_name, _, rate = read_accelerometer.read_file(acc_filename)
        for jaxis in range(3):
            fmotor = motor_cal_func(hk_data[motor_value]['voltage'])
            freq_peak, psd_peak = find_psd_peaks(acc_name[:,jaxis], rate,
                                                 freq_range=[fmotor-2.0, fmotor+2.0],
                                                 averaging=False,
                                                 plot=psd_plots,
                                                 plot_filename='psd_peak_{}axis_{:.1f}.png'\
                                                                .format(axes[jaxis], motor_value))
            psd_data[motor_value][axes[jaxis]] = dict()
            psd_data[motor_value][axes[jaxis]]['freq'] = freq_peak
            psd_data[motor_value][axes[jaxis]]['psd'] = psd_peak
            psd_data[motor_value][axes[jaxis]]['motor_voltage'] = \
                                        hk_data[motor_value]['voltage']

    return psd_data


if __name__ == '__main__':
    P = ap.ArgumentParser(description='Analyze frequency sweep data.',
                          formatter_class=ap.ArgumentDefaultsHelpFormatter)
    P.add_argument('hkfilename', type=str,
                   help='Filename with housekeeping data to load.')
    P.add_argument('--data-path', type=str, default=None,
                   help='Path to raw accelerometer data to read.')
    P.add_argument('--output-filename', type=str, default='psd_tf_data.pkl',
                   help='Name of output file to save.')
    P.add_argument('--save-plots', action='store_true',
                   help='Save plot for each PSD showing peak location found.')
    args = P.parse_args()

    psd_data = analyze_psds(args.hkfilename, data_path=args.data_path,
                           psd_plots=args.save_plots)
    with open(args.output_filename, 'wb') as f:
        pickle.dump(psd_data, f)
