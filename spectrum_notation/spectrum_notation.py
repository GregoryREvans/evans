import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft,fftfreq

samplerate, data = wavfile.read("/Users/evansdsg2/evans/spectrum_notation/Test_Tones.wav")
samples = data.shape[0]
# plt.plot(data[:200])

datafft = fft(data)
#Get the absolute value of real and complex component:
fftabs = abs(datafft)
freqs = fftfreq(samples,1/samplerate)
# plt.plot(freqs,fftabs)

# plt.xlim( [10, samplerate/2] )
# plt.xscale( 'log' )
# plt.grid( True )
# plt.xlabel( 'Frequency (Hz)' )
# plt.plot(freqs[:int(freqs.size/2)],fftabs[:int(freqs.size/2)])

samplerate, data = wavfile.read("/Users/evansdsg2/evans/spectrum_notation/Test_Tones.wav")
data.shape
samples = data.shape[0]
# plt.plot(data[:4*samplerate]) #plot first 4 seconds
data = data[:,0]
data.shape
# plt.plot(data[:4*samplerate]) #plot first 4 seconds

datafft = fft(data)
#Get the absolute value of real and complex component:
fftabs = abs(datafft)
freqs = fftfreq(samples,1/samplerate)
plt.xlim( [10, samplerate/2] )
plt.xscale( 'log' )
plt.grid( True )
plt.xlabel( 'Frequency (Hz)' )
plt.plot(freqs[:int(freqs.size/2)],fftabs[:int(freqs.size/2)]
