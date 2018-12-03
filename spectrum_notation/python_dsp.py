import scipy.io.wavfile
import numpy as np
import matplotlib

rate,audData=scipy.io.wavfile.read("/Users/evansdsg2/evans/spectrum_notation/Test_Tones.wav")

# print(rate)
# print(audData)
# print(audData.shape[0] / rate)
# print(audData.shape[1])
channel1=audData[:,0]#left
channel2=audData[:,1]#right
# print(channel1)
# print(channel2)
# print(audData.dtype)

#energy of file
# print(np.sum(channel1.astype(float)**2))
# print(1.0/(2*(channel1.size)+1)*np.sum(channel1.astype(float)**2)/rate)

#create a time variable in seconds
time = np.arange(0, float(audData.shape[0]), 1) / rate
#plot amplitude (or loudness) over time
matplotlib.pyplot.figure(1)
matplotlib.pyplot.subplot(211)
matplotlib.pyplot.plot(time, channel1, linewidth=0.01, alpha=0.7, color='#ff7f00')
matplotlib.pyplot.xlabel('Time (s)')
matplotlib.pyplot.ylabel('Amplitude')
matplotlib.pyplot.subplot(212)
matplotlib.pyplot.plot(time, channel2, linewidth=0.01, alpha=0.7, color='#ff7f00')
matplotlib.pyplot.xlabel('Time (s)')
matplotlib.pyplot.ylabel('Amplitude')
matplotlib.pyplot.show()

#TO BE CONTINUED
