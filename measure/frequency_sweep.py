import argparse as ap
import numpy as np
from python_tb6612fng.TB6612FNG import TB6612FNG
from python_mma8451.record_accelerometer import MMA8451DAQ

P = ap.ArgumentParser(description='Perform frequency sweep to measure '
                      'mechanical transfer function.',
                      formatter_class=ap.ArgumentDefaultsHelpFormatter)
P.add_argument('voltage', type=float,
               help='Power supply voltage setting used for motor drive.')
P.add_argument('motor', choices=['JQ24-35F580C'],
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

motor_ranges = np.linspace(args.motor_range[0], args.motor_range[1], args.n_voltages)

motor = TB6612FNG()
daq = MMA8451DAQ()

motor.output_on(0)
for motor_range in motor_ranges:
    # set motor controller range
    motor.set_pwm(motor_range)
    
    # take data for a specified duration
    daq.run(args.duration)
