# fftDnaMods
A simple python script to work with 2-column tables and do some FFT stuff.


Many thanks to Kevin Urban at Early Signal (kevin.urban@earlysignal.org) for his valuable insights on FFT analysis of sequence data.  



Example usage:

# Get example data out
tar -xzf example-data.tar.gz

# Run script with defaults
fftForDnaMods.py spacing*txt

# Same as
fftForDnaMods.py -c 200 -r 10 spacing*txt


## Options:
--cutoff/-c  Just says to only look at X values (bp lengths) up to this high.
--rmedge/-r  Gives it a fudge factor to ignore edges of power array when looking for maximum power position.


## This script is obviously very simple in terms of finding a single max peak value.


