import abjad
import evans

staff = abjad.Staff([abjad.Voice("c'4 c'4 c'4 c'4", name="Voice 1")], name="Staff 1")

h = evans.GettatoHandler()

h(staff)

for voice in abjad.iterate(staff).components(abjad.Staff):
    print(voice.name)
    abjad.f(voice)
