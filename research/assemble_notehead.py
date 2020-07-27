import abjad


def assemble_notehead(head_dur):
    pair = head_dur.pair
    dot_parts = []
    while 1 < pair[0]:
        dot_part = (1, pair[1])
        dot_parts.append(dot_part)
        head_dur -= abjad.Duration(dot_part)
        pair = head_dur.pair
    duration_string = f"{pair[1]}"
    for _ in dot_parts:
        duration_string += "."
    return duration_string


print(assemble_notehead(abjad.Duration(3, 8)))

tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
inner_durs = []
for _ in tuplet[:]:
    if isinstance(_, abjad.Tuplet):
        inner_durs.append(_.multiplied_duration)
    else:
        inner_durs.append(_.written_duration)
tuplet_dur = sum(inner_durs)
imp_num, imp_den = tuplet.implied_prolation.pair
head_dur = tuplet_dur / imp_den
dur = head_dur * imp_num
dur
