import abjad

class NoteheadBracketMaker:

    def __call__(self, selections):
        return self._transform_brackets(selections)

    def _transform_brackets(self, selections):
        for tuplet in abjad.select(selections).components(abjad.Tuplet):
            # written_duration = abjad.inspect(tuplet).duration().equal_or_greater_assignable
            time_duration = tuplet.multiplied_duration
            # print(time_duration)
            time_denominator = time_duration.denominator
            # print(time_denominator)
            imp_num, imp_den = tuplet.implied_prolation.pair
            # print(imp_num)
            notehead_wrapper = time_denominator * imp_num #can't just be the denominator because something like 3/8 divided by 3 = 1/8 but just the denominator "8" doesn't give us enough information to go by
            multiplier = 1
            abjad.tweak(tuplet).TupletNumber.text = f'#(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text {imp_den * multiplier} {imp_num * multiplier}) "{notehead_wrapper}")'
        return selections

# ###DEMO###
# tuplet = abjad.Tuplet((3, 2), "cs'8 d'8")
# tuplet_2 = abjad.Tuplet((2, 3), components=[abjad.Note(0, (3, 8)), tuplet])
# staff = abjad.Staff()
# staff.append(tuplet_2)
# new_brackets = NoteheadBracketMaker()
# new_brackets(staff)
# abjad.f(staff)
# abjad.show(staff)
