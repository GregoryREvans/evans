import abjad
tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
staff = abjad.Staff()
staff.append(tuplet)
for tuplet in abjad.select(staff).components(abjad.Tuplet):
    duration = abjad.inspect(tuplet).duration()
    implied_prolation_pair = tuplet.implied_prolation
    pair = implied_prolation_pair.pair
    denominator_pair = duration.pair
    denominator = denominator_pair[-1]
    print(f'denominator of {denominator}!')
    notehead_wrapper = denominator * pair[0]
    literal = abjad.LilyPondLiteral(r'\tweak TupletNumber.text #(tuplet-number::append-note-wrapper' + f'(tuplet-number::non-default-tuplet-fraction-text {pair[-1]} {pair[0]}) "{notehead_wrapper}")', format_slot='before')
    abjad.attach(literal, tuplet)
abjad.show(staff)
