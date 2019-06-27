import abjad
import pyaudio
import wave
import numpy as np
import abjadext.rmakers

freq_list = []

chunk = 2048

# open up a wave
wf = wave.open("/Users/evansdsg2/evans/hello.wav", "rb")
swidth = wf.getsampwidth()
RATE = wf.getframerate()
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=RATE,
    output=True,
)

# read some data
data = wf.readframes(chunk)
# play stream and find the frequency of each chunk
while len(data) == chunk * swidth:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window
    # Take the fft and square each value
    fftData = abs(np.fft.rfft(indata)) ** 2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1 : which + 2 :])
        x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which + x1) * RATE / chunk
        freq_list.append(thefreq)
    else:
        thefreq = which * RATE / chunk
        freq_list.append(thefreq)
    # read some more data
    data = wf.readframes(chunk)
if data:
    stream.write(data)
stream.close()
p.terminate()

pitches = [abjad.NumberedPitch.from_hertz(x) for x in freq_list]

notes = [abjad.Note(x, abjad.Duration(1, 8)) for x in pitches]

staff = abjad.Staff(notes)
clef = abjad.Clef("varC")
time_signature = abjad.TimeSignature((11, 8))
abjad.attach(time_signature, staff[0])
abjad.attach(clef, staff[0])
score = abjad.Score()
score.append(staff)

for staff in abjad.select(score).components(abjad.Staff):
    specifier = abjadext.rmakers.BeamSpecifier(beam_each_division=False)
    specifier(staff[:])
    abjad.beam(staff[:], beam_lone_notes=False, beam_rests=False)

lilyfile = abjad.LilyPondFile.new(
    score,
    includes=[
        "/Users/evansdsg2/evans/abjad_functions/talea_timespan/first_stylesheet_two.ily"
    ],
)

abjad.show(lilyfile)
# abjad.play(lilyfile)
