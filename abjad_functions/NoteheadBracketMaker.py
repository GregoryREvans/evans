import abjad

class NoteheadBracketMaker:

    def __call__(self, selections):
        return self._transform_brackets(selections)

    def _transform_brackets(self, selections):
        for tuplet in abjad.select(selections).components(abjad.Tuplet):
            written_duration = abjad.inspect(tuplet).duration().equal_or_greater_assignable
            denominator = written_duration.denominator
            imp_num, imp_den = tuplet.implied_prolation.pair
            notehead_wrapper = denominator * imp_num
            abjad.tweak(tuplet).TupletNumber.text = abjad.LilyPondLiteral(f'(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text {imp_den} {imp_num}) "{notehead_wrapper}")')
            # literal = abjad.LilyPondLiteral(r'\tweak TupletNumber.text #(tuplet-number::append-note-wrapper' + f'(tuplet-number::non-default-tuplet-fraction-text {imp_den} {imp_num}) "{notehead_wrapper}")', format_slot='absolute_before')
            # abjad.attach(literal, tuplet)
        return selections

###DEMO###
tuplet = abjad.Tuplet((3, 2), "c'8 d'8")
tuplet_2 = abjad.Tuplet((2, 3), components=[abjad.Note(0, (1, 2)), tuplet])
staff = abjad.Staff()
staff.append(tuplet_2)
new_brackets = NoteheadBracketMaker()
new_brackets(staff)
abjad.show(staff)
