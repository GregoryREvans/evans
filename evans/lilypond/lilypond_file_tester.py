import abjad
from abjadext import microtones


ratios = [f"{_ + 1}/1" for _ in range(11)]
notes = [abjad.Note("a,,,32") for _ in ratios]
for note, ratio in zip(notes, ratios):
    microtones.tune_to_ratio(note.note_head, ratio)
staff = abjad.Staff()
staff.extend(notes)
lilypond_file = abjad.LilyPondFile.new(
    staff, includes=["/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily", "/Users/evansdsg2/abjad/docs/source/_stylesheets/heji2-accidental-markups.ily"],
)
style = '"dodecaphonic"'
lilypond_file.layout_block.items.append(fr"\accidentalStyle {style}" )
abjad.show(lilypond_file) # doctest: +SKIP
