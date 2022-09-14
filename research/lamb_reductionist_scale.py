import abjad
import evans

partials = evans.reduced_spectrum(29, 192, evans.reduce_list_by_prime_limit)


def force_accidental(selections):
    ties = abjad.select.logical_ties(selections, pitched=True)
    for tie in ties:
        first_leaf = tie[0]
        if isinstance(first_leaf, abjad.Note):
            first_leaf.note_head.is_forced = True
        elif isinstance(first_leaf, abjad.Chord):
            heads = first_leaf.note_heads
            for head in heads:
                head.is_forced = True
        else:
            ex = f"Object must be of type {type(abjad.Note())} or {type(abjad.Chord())}"
            raise Exception(ex)


staff = abjad.Staff([abjad.Note("c,,,4") for _ in partials])
handler = evans.PitchHandler([f"{_}/1" for _ in partials], forget=False, as_ratios=True)
handler(staff)
staff.append(abjad.Rest("r4"))
clef = evans.ClefHandler(
    clef="bass",
    add_extended_clefs=True,
    add_ottavas=True,
)
clef(staff)
force_accidental(staff)
score = abjad.Score([staff])
moment = "#(ly:make-moment 1 25)"
abjad.setting(score).proportional_notation_duration = moment
file = abjad.LilyPondFile(
    items=[
        r'\include "/Users/gregoryevans/abjad/abjad/scm/abjad.ily"',
        r'\include "/Users/gregoryevans/abjad-ext-microtones/abjadext/microtones/lilypond/ekmelos-ji-accidental-markups.ily"',
        score,
    ],
)
abjad.show(file)
