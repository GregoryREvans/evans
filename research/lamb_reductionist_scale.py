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
for note, partial in zip(abjad.select.notes(score), partials):
    markup = abjad.Markup(rf"\markup {partial}")
    bundle = abjad.bundle(
        markup,
        r"- \tweak color #red",
    )
    abjad.attach(bundle, note, direction=abjad.DOWN)
moment = "#(ly:make-moment 1 25)"
abjad.setting(score).proportional_notation_duration = moment
paper = abjad.Block(
    "paper",
    items=[
        r"""
    system-system-spacing = #'(
        (basic-distance . 0)
        (minimum-distance . 20) % space after each system
        (padding . 0)
        (stretchability . 0)
    )
    """
    ],
)
block = abjad.Block(
    "layout",
    items=[
        r"""
    indent = #0
    \context {
        \Score
        \remove Bar_number_engraver
        \override Stem.stencil = ##f
        autoBeaming = ##f
    }
    \context {
        \Staff
        \override TimeSignature.stencil = ##f
    }
    """,
    ],
)
file = abjad.LilyPondFile(
    items=[
        r'\version "2.23.81"',
        r'\language "english"',
        r'\include "/Users/gregoryevans/abjad/abjad/scm/abjad.ily"',
        """#(set-default-paper-size "letterlandscape")""",
        """#(set-global-staff-size 13)""",
        r'\include "/Users/gregoryevans/abjad-ext-microtones/abjadext/microtones/lilypond/ekmelos-ji-accidental-markups.ily"',
        block,
        paper,
        score,
    ],
)
abjad.show(file)
