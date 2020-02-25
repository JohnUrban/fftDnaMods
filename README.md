# fftDnaMods
A simple python script to work with 2-column tables and do some FFT stuff.


Many thanks to Kevin Urban at Early Signal (kevin.urban@earlysignal.org) and Cohen Veterans Bioscience (https://www.cohenveteransbioscience.org/our-team/) for his valuable insights on FFT analysis of sequence data.  



# Example usage:

>Get example data out:

tar -xzf example-data.tar.gz

>Run script with defaults:

fftForDnaMods.py spacing*txt

>Same as:

fftForDnaMods.py -c 200 -M 100 spacing*txt


>To also generate Frequency vs Power plots, do:

fftForDnaMods.py --plot png -c 200 -M 100 spacing*txt

or

fftForDnaMods.py --plot pdf -c 200 -M 100 spacing*txt



## Options:
--cutoff/-c  Just says to only look at X values (bp lengths) up to this high.

--max_period/-M  Allows one to look for the max power peak periodicity excluding periods greater than this.



This script is obviously very simple in terms of finding a single max peak value.



If you find these tools useful for your own work, please cite the fungus fly genome preprint:
----------------------------------------------------------------------------------
Urban JM, Foulk MS, Bliss JE, Coleman CM, Lu N, Mazloom R, Brown SJ, Spradling $

Single-molecule sequencing of long DNA molecules allows high contiguity de novo$

bioRxiv 2020.02.24.963009.

https://www.biorxiv.org/content/10.1101/2020.02.24.963009v1

