import abjad

tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
tuplet_2 = abjad.Tuplet((2, 3), components=[abjad.Note(0, (1, 2)), tuplet])
staff = abjad.Staff()
staff.append(tuplet_2)

for tuplet in abjad.select(staff).components(abjad.Tuplet):
    written_duration = abjad.inspect(tuplet).duration().equal_or_greater_assignable
    denominator = written_duration.denominator
    imp_num, imp_den = tuplet.implied_prolation.pair
    notehead_wrapper = denominator * imp_num
    literal = abjad.LilyPondLiteral(
        r"\tweak TupletNumber.text #(tuplet-number::append-note-wrapper"
        + f'(tuplet-number::non-default-tuplet-fraction-text {imp_den} {imp_num}) "{notehead_wrapper}")',
        format_slot="before",
    )
    abjad.attach(literal, tuplet)
abjad.show(staff)
