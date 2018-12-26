import abjad

staff = abjad.Staff("c'4 ~ c'8")
for tie in abjad.select(staff).logical_ties(pitched=True):
    literal = abjad.LilyPondLiteral('% this is a comment', format_slot='before')
    for leaf in abjad.select(tie).leaves(pitched=True):
        abjad.attach(literal, leaf)
abjad.show(tie)
