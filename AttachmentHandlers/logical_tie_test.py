import abjad

staff = abjad.Staff("c'4 ~ c'8")
# for tie in abjad.select(staff).logical_ties(pitched=True):
#     string = str(r"""\once \override Staff.NoteHead.style = #'cross""")
#     literal = abjad.LilyPondLiteral(string, format_slot='before')
#     for leaf in abjad.select(tie).leaves(pitched=True):
#         abjad.attach(literal, leaf)
# abjad.show(tie)

def cyc(lst):
    count = 0
    while True:
        yield lst[count%len(lst)]
        count += 1
        
_cyc_noteheads = cyc(['cross', ])

def add_noteheads(selections):
    head = _cyc_noteheads
    for tie in abjad.select(selections).logical_ties(pitched=True):
        head_name = next(head)
        string = str(r"""\once \override Staff.NoteHead.style = #'""")
        full_string = string + head_name
        style = abjad.LilyPondLiteral(full_string, format_slot='before',)
        for leaf in abjad.select(tie).leaves(pitched=True):
            abjad.attach(style, leaf)
    return selections

add_noteheads(staff)

abjad.show(staff)
