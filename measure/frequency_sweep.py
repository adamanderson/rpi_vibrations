import argparse as ap
import numpy as np
from python_tb6612fng.TB6612FNG import TB6612FNG
from python_mma8451.record_accelerometer import MMA8451DAQ
import pickle
from datetime import datetime
import time

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

    # save housekeeping data
    daq = MMA8451DAQ('motor={:.1f}'.format(motor_range))
    hkdata[motor_range] = {'voltage': args.voltage * (motor_range / 100.),
                           'file': daq.fname}
    with open(datetime.utcnow().strftime('%Y%m%d_%H%M%S_sweep_housekeeping.pkl'), 'w') as f:
        pickle.dump(hkdata, f)
    
    # take data for a specified duration
    daq.run(args.duration)
