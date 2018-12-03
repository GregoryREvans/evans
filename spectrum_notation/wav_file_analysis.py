import math
from scipy.io import wavfile
from scipy import fft
from numpy import arange

sampFreq, snd = wavfile.read('/Users/evansdsg2/evans/spectrum_notation/Test_Tones.wav')
snd = snd / (2.**15)
s1 = snd[:,0]

timeArray = arange(0, 5292, 1)
timeArray = timeArray / sampFreq
timeArray = timeArray * 1000  #scale to milliseconds

n = len(s1)
p = fft(s1) # take the fourier transform

c = math.ceil((n+2)/2.0)

nUniquePts = int(c)
p = p[0:nUniquePts]
p = abs(p)

p = p / float(n) # scale by the number of points so that
                 # the magnitude does not depend on the length
                 # of the signal or on its sampling frequency
p = p**2  # square it to get the power

# multiply by two (see technical document for details)
# odd nfft excludes Nyquist point
if n % 2 > 0: # we've got odd number of points fft
    p[1:len(p)] = p[1:len(p)] * 2
else:
    p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft

freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n);
print(freqArray)
