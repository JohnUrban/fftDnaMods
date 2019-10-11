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
22	228
23	180
24	145
25	141
26	195
27	222
28	310
29	302
30	399
31	295
32	242
33	191
34	133
35	150
36	162
37	234
38	270
39	334
40	378
41	339
42	232
43	163
44	141
45	117
46	155
47	171
48	203
49	356
50	337
51	313
52	233
53	218
54	119
55	101
56	139
57	181
58	207
59	271
60	302
61	303
62	226
63	242
64	157
65	136
66	132
67	167
68	172
69	242
70	277
71	298
72	253
73	188
74	140
75	119
76	105
77	140
78	163
79	252
80	233
81	279
82	237
83	208
84	165
85	153
86	117
87	102
88	136
89	218
90	255
91	228
92	247
93	199
94	156
95	137
96	139
97	97
98	130
99	188
100	205
101	249
102	260
103	201
104	157
105	152
106	117
107	120
108	131
109	158
110	209
111	211
112	228
113	261
114	190
115	141
116	129
117	137
118	122
119	140
120	185
121	253
122	233
123	208
124	157
125	168
126	121
127	118
128	165
129	124
130	160
131	195
132	207
133	200
134	196
135	154
136	121
137	124
138	124
139	121
140	174
141	209
142	216
143	251
144	228
145	190
146	115
147	109
148	127
149	152
150	138
151	207
152	220
153	201
154	195
155	162
156	138
157	110
158	112
159	109
160	121
161	161
162	181
163	178
164	191
165	179
166	136
167	111
168	117
169	95
170	108
171	127
172	142
173	183
174	249
175	167
176	153
177	125
178	120
179	117
180	118
181	127
182	151
183	178
184	190
185	192
186	127
187	127
188	130
189	112
190	115
191	146
192	128
193	149
194	178
195	152
196	166
197	125
198	115
199	140
200	98

""", formatter_class= argparse.RawTextHelpFormatter)


parser.add_argument('files', metavar='files', nargs='*',
                   type= str, 
                   help='''Paths to as many tables as you want. 
                        This can also be left empty for standard in or specified as - or stdin.''')

parser.add_argument('-c', '--cutoff', type=int, default=200,
                    help='''Only use X values <= cutoff. Default=200.''')
parser.add_argument('-r', '--rmedge', type=int, default=10,
                    help='''When looking for periodicity length, in addition to using the entire power array, also get the value after cutting this many values off the edges of the power array (helps in cases where edges have highest values).''')

args = parser.parse_args()


# Functions
def fft(fh, cutoff=200, rmedge=10):
        
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

    i = power.argmax() 
    bp_withedge = 1.0/freqs[i]
    i = power[rmedge:-rmedge].argmax() 
    bp_rmedges = 1.0 / freqs[rmedge:-rmedge][i]
    return os.path.basename(fh), bp_withedge, bp_rmedges


def main(args):
    # Loop
    for fh in args.files:
        print '\t'.join([str(e) for e in fft(fh, args.cutoff, args.rmedge)])




## Execute
try:
    main(args)
except IOError:
    pass
                


