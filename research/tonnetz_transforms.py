import abjad
from abjadext import microtones
from quicktions import Fraction

# major
source = microtones.RatioSegment(
    [
        1,
        "17/1",
        "9/1",
        "19/1",
        "5/1",
        "11/1",
        "23/1",
        "3/1",
        "25/1",
        "13/1",
        "7/1",
        "15/1",
    ]
)
Ms = source.constrain_to_octave()
Msp = Ms.invert(Ms[0]).multiply(Fraction(3, 2))
Msl = Msp.multiply(Fraction(5, 4))
Msr = Msp.multiply(Fraction(5, 3))
Ms71 = Msp.multiply(Fraction(7, 4))
Ms75 = Msp.multiply(Fraction(7, 5))
Ms73 = Msp.multiply(Fraction(7, 6))

triads_1 = [Ms, Msp, Msl, Msr, Ms71, Ms75, Ms73]

score = abjad.Score()

for chord in triads_1:
    staff = abjad.Staff([abjad.Note("c'8") for pitch in chord])
    for pitch, note in zip(chord, staff):
        m = microtones.tune_to_ratio(note.note_head, pitch, return_cent_markup=True)
        abjad.attach(m, note)
    abjad.attach(abjad.Clef("treble"), staff[0])
    abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
    score.append(staff)

# minor

ms = source.invert().constrain_to_octave()
msp = ms.invert(ms[0]).multiply(Fraction(2, 3)).multiply(3).constrain_to_octave()
msl = msp.multiply(Fraction(4, 5)).multiply(3).constrain_to_octave()
msr = msp.multiply(Fraction(3, 5)).multiply(3).constrain_to_octave()
ms71 = msp.multiply(Fraction(4, 7)).multiply(3).constrain_to_octave()
ms75 = msp.multiply(Fraction(5, 7)).multiply(3).constrain_to_octave()
ms73 = msp.multiply(Fraction(6, 7)).multiply(3).constrain_to_octave()
ms = ms.multiply(3).constrain_to_octave()

triads_2 = [ms, msp, msl, msr, ms71, ms75, ms73]

for chord in triads_2:
    staff = abjad.Staff([abjad.Note("c'8") for pitch in chord])
    for pitch, note in zip(chord, staff):
        m = microtones.tune_to_ratio(note.note_head, pitch, return_cent_markup=True)
        abjad.attach(m, note)
    abjad.attach(abjad.Clef("treble"), staff[0])
    abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
    score.append(staff)

lilypond_file = abjad.LilyPondFile.new(
    score,
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/ekmelos-ji-accidental-markups.ily",
    ],
)
style = '"dodecaphonic"'
lilypond_file.layout_block.items.append(fr"\accidentalStyle {style}")
abjad.show(lilypond_file)

final_triads = triads_1 + triads_2
final_triads_hertz = []
for s in final_triads:
    hertz_list = [abjad.NamedPitch("e'").hertz * _ for _ in s]
    final_triads_hertz.append(hertz_list)

print(final_triads_hertz)
