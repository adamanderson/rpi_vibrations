import argparse as ap
import numpy as np
from python_tb6612fng.TB6612FNG import TB6612FNG
from python_mma8451.record_accelerometer as MMA8451DAQ

P = ap.ArgumentParser(description='Take PSD during observations.',
                      formatter_class=ap.ArgumentDefaultsHelpFormatter)
P.add_argument('--duration', type=float, default=None,
               help='Duration of accelerometer data (in seconds).')
args = P.parse_args()

daq = MMA8451DAQ()

# take data for a specified duration
daq.run(args.duration)
