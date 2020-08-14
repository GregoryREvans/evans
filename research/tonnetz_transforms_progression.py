import abjad
import evans
from abjadext import microtones

score = abjad.Score()

source = microtones.RatioSegment([1, "5/4", "3/2",])

triads = evans.tonnetz(
    source, "major", ["p", "h", "s", "n", "p", "l", "r", "r", "l", "l",]
)

for chord in triads:
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

final_triads_hertz = []
for s in triads:
    hertz_list = [abjad.NamedPitch("e'").hertz * _ for _ in s]
    final_triads_hertz.append(hertz_list)

print(final_triads_hertz)
