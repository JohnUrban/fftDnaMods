#!/usr/bin/env python2.7
import sys, os, argparse
import numpy as np
from collections import defaultdict
import pandas as pd



parser = argparse.ArgumentParser(description="""

Given a 2 column table of X and Y coordinates, do FFT analysis and return X value with highest power.

See a wave pattern?
Can eyeball a periodicity?

Use this for a mathy way to do it.

Use case:
X = bp length
Y = number of times X was seen.


Example data:
0	415
1	365
2	247
3	465
4	177
5	152
6	244
7	402
8	358
9	568
10	723
11	385
12	246
13	183
14	180
15	180
16	182
17	263
18	349
19	471
20	406
21	407
....
Etc
See example-data.tar.gz for more.


""", formatter_class= argparse.RawTextHelpFormatter)


parser.add_argument('files', metavar='files', nargs='*',
                   type= str, 
                   help='''Paths to as many tables as you want. 
                        This can also be left empty for standard in or specified as - or stdin.''')

parser.add_argument('-c', '--cutoff', type=int, default=200,
                    help='''Only use X values <= cutoff. Default=200.''')


parser.add_argument('-M', '--max_period', type=int, default=100,
                    help='''When looking for periodicity length, in addition to using the entire power array, also get the value when only looking at periods <= this value. Example default would be 100.''')



args = parser.parse_args()


# Functions
def fft(fh, cutoff=200, max_period=100):
    df = pd.read_csv(fh, sep='\t', header=None, names=['bptime','activation'])
    df = df[df['bptime']<=cutoff]
    N = len(df.activation)
    hann = np.hanning(N)
    mean = df.activation.mean()
    signal = hann*(df.activation - mean)

    bp_fft = np.fft.fft(signal)
    power = np.square(np.absolute(bp_fft))
    freqs = np.fft.fftfreq(N)
    index = freqs > 0
    freqs = freqs[index]
    power = power[index]
    periodicity = 1.0/freqs
    
    i = power.argmax()
    bp_withedge = periodicity[i]
    #i = power[rmedge:-rmedge].argmax()
    #bp_rmedges = periodicity[rmedge:-rmedge][i]
    i = power[periodicity <= max_period].argmax()
    bp_maxper = periodicity[periodicity <= max_period][i]
    return os.path.basename(fh), bp_withedge, bp_maxper


def main(args):
    # Loop
    for fh in args.files:
        print '\t'.join([str(e) for e in fft(fh, args.cutoff, args.max_period)])




## Execute
try:
    main(args)
except IOError:
    pass
                


