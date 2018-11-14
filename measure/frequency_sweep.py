import argparse as ap
import numpy as np
from python_tb6612fng.TB6612FNG import TB6612FNG
from python_mma8451.record_accelerometer import MMA8451DAQ
import pickle
from datetime import datetime
import time
import os

P = ap.ArgumentParser(description='Perform frequency sweep to measure '
                      'mechanical transfer function.',
                      formatter_class=ap.ArgumentDefaultsHelpFormatter)
P.add_argument('voltage', type=float,
               help='Power supply voltage setting used for motor drive.')
P.add_argument('--motor', choices=['JQ24-35F580C'], default='JQ24-35F580C',
               help='Type of motor used for vibration.')
P.add_argument('--motor-range', type=float, nargs=2, default=[0,100],
               help='Min and max of range of motor voltages to apply. Both '
               'upper and lower values must be between 0 and 100 inclusive.')
P.add_argument('--n-voltages', type=int, default=10,
               help='Number of voltages at which to take measurements.')
P.add_argument('--duration', type=float, default=10,
               help='Duration of accelerometer data (in seconds) to take at '
               'each voltage step.')
P.add_argument('--gcp-noise-stare', action='store_true',
               help='Take a noise stare through GCP.')
P.add_argument('--noise-stare-duration', type=float, default=60.0,
               help='Duration of the GCP noise stare in seconds. Note that '
               'a 1m noise stare takes 4m to execute because of associated '
               'calibrator stare in the schedule.')
args = P.parse_args()

# check parameter ranges
if args.motor_range[0] < 0 or args.motor_range[0] > 100 or \
   args.motor_range[1] < 0 or args.motor_range[1] > 100:
    raise ValueError('Argument `--motor-range` out of allowed range.')
if args.motor_range[0] > args.motor_range[1]:
    raise ValueError('Upper end of `--motor-range` arugment is less than '
                     'lower end.')

# housekeeping data
hkdata = {}
hkfilename = datetime.utcnow().strftime('%Y%m%d_%H%M%S_sweep_housekeeping.pkl')

motor_ranges = np.linspace(args.motor_range[0], args.motor_range[1], args.n_voltages)
motor = TB6612FNG()
motor.output_on(0)

# take background measurment with motors off
if 0.0 not in motor_ranges:
    motor_ranges = np.insert(motor_ranges, 0, 0)
    
# actually take the data
for motor_range in motor_ranges:
    print('Setting motor to {}%.'.format(motor_range))

    # set motor controller range
    motor.set_pwm(motor_range)
    time.sleep(1.0) # wait time after to allow time for equilibration
    
    # start a noise stare if requested
    if args.gcp_noise_stare:
        stare_length = args.noise_stare_duration / 60.0
        os.system('ssh sptdaq@192.168.2.4 "source ~/.bash_profile; '
                  '/home/sptdaq/code/gcp/build/bin/sptCommand host=control.spt '
                  'command=\'schedule noise_stare_no_acquire_20170910.sch( {:.0f}m )\'"'.format(stare_length))
    time.sleep(10)

    daq = MMA8451DAQ('motor={:.1f}'.format(motor_range))
    
    # save housekeeping data
    hkdata[motor_range] = {'voltage': args.voltage * (motor_range / 100.),
                           'file': daq.fname,
                           'time': datetime.utcnow()}
    with open(hkfilename, 'wb') as f:
        pickle.dump(hkdata, f)
    
    # take data for a specified duration
    daq.run(args.duration)
    time.sleep(1)
