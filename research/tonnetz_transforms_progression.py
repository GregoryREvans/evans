import abjad
from abjadext import microtones
from quicktions import Fraction

score = abjad.Score()

# major
# source = microtones.RatioSegment([1, "17/1", "9/1", "19/1", "5/1", "11/1", "23/1", "3/1", "25/1", "13/1", "7/1", "15/1"])
source = microtones.RatioSegment([1, "5/1", "3/1", "7/1", "9/1"])
Ms = source.constrain_to_octave()
Msp = Ms.invert(Ms[0]).multiply(Fraction(3, 2)).constrain_to_octave()
msp = Msp.invert(Msp[0]).multiply(Fraction(2, 3)).multiply(3).constrain_to_octave()
Msl = (
    msp.invert(msp[0])
    .multiply(Fraction(3, 2))
    .multiply(Fraction(5, 4))
    .constrain_to_octave()
)
msl = (
    Msl.invert(Msl[0])
    .multiply(Fraction(2, 3))
    .multiply(3)
    .multiply(Fraction(4, 5))
    .multiply(3)
    .constrain_to_octave()
)
Msr = (
    msl.invert(msl[0])
    .multiply(Fraction(3, 2))
    .multiply(Fraction(5, 3))
    .constrain_to_octave()
)
msr = (
    Msr.invert(Msr[0])
    .multiply(Fraction(2, 3))
    .multiply(3)
    .multiply(Fraction(3, 5))
    .multiply(3)
    .constrain_to_octave()
)
Ms71 = (
    msr.invert(msr[0])
    .multiply(Fraction(3, 2))
    .multiply(Fraction(7, 4))
    .constrain_to_octave()
)
ms71 = (
    Ms71.invert(Ms71[0])
    .multiply(Fraction(2, 3))
    .multiply(3)
    .multiply(Fraction(4, 7))
    .multiply(3)
    .constrain_to_octave()
)
Ms75 = (
    ms71.invert(ms71[0])
    .multiply(Fraction(3, 2))
    .multiply(Fraction(7, 5))
    .constrain_to_octave()
)
ms75 = (
    Ms75.invert(Ms75[0])
    .multiply(Fraction(2, 3))
    .multiply(3)
    .multiply(Fraction(5, 7))
    .multiply(3)
    .constrain_to_octave()
)
Ms73 = (
    ms75.invert(ms75[0])
    .multiply(Fraction(3, 2))
    .multiply(Fraction(7, 6))
    .constrain_to_octave()
)
ms73 = (
    Ms73.invert(Ms73[0])
    .multiply(Fraction(2, 3))
    .multiply(3)
    .multiply(Fraction(6, 7))
    .multiply(3)
    .constrain_to_octave()
)

triads_2 = [
    Ms,
    Msp,
    msp,
    Msl,
    msl,
    Msr,
    msr,
    Ms71,
    ms71,
    Ms75,
    ms75,
    Ms73,
    ms73,
]

for i, _ in enumerate(triads_2):
    triads_2[i] = _.multiply(Fraction(1, 2))

for chord in triads_2:
    staff = abjad.Staff([abjad.Note("c'8") for pitch in chord])
    for pitch, note in zip(chord, staff):
        m = microtones.tune_to_ratio(note.note_head, pitch, return_cent_markup=True)
        abjad.attach(m, note)
    abjad.attach(abjad.Clef("treble"), staff[0])
    # abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
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

final_triads = triads_2
final_triads_hertz = []
for s in final_triads:
    hertz_list = [abjad.NamedPitch("e'").hertz * _ for _ in s]
    final_triads_hertz.append(hertz_list)

print(final_triads_hertz)
