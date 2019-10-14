#!/usr/bin/env python2.7
import sys, os, argparse
import numpy as np
from collections import defaultdict
import pandas as pd
from matplotlib import pyplot as plt


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


parser.add_argument('-M', '--max_period', type=int, default=1000000000000,
                    help='''When looking for periodicity length, in addition to using the entire power array, also get the value when only looking at periods <= this value. Example setting would be 100. Defaults to very high number to include all (1e12).''')

parser.add_argument('-P', '--plot', type=str, default=False,
                    help='''Make plots.... Provide 'pdf', 'png', 'jpg',... as argument.''')



args = parser.parse_args()


# Functions
def fft(fh, cutoff=200, max_period=10000000000000, plot=False):
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
    
    #i = power.argmax()
    #bp_withedge = periodicity[i]
    #power_withedge = power[i]
    #i = power[rmedge:-rmedge].argmax()
    #bp_rmedges = periodicity[rmedge:-rmedge][i]
    i = power[periodicity <= max_period].argmax()
    maxbp = periodicity[periodicity <= max_period][i]
    maxpower = power[periodicity <= max_period][i]
    if plot:
        plt.plot(freqs,power)
        plt.xlabel("Frequency (1/periodicity)")
        plt.ylabel("Power")
        plt.title(os.path.basename(fh))
        plt.savefig('plot.'+os.path.basename(fh)+'.'+plot)   
        plt.close() 
    return os.path.basename(fh), maxbp, maxpower 


def main(args):
    # Loop
    for fh in args.files:
        print '\t'.join([str(e) for e in fft(fh, args.cutoff, args.max_period, args.plot)])




## Execute
try:
    main(args)
except IOError:
    pass
                


