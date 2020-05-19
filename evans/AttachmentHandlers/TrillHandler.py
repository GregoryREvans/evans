import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class TrillHandler:
    def __init__(
        self, boolean_vector=[0], continuous=True, count=-1, name="Trill Handler"
    ):
        self.continuous = continuous
        self._count = count
        self.boolean_vector = CyclicList(boolean_vector, self.continuous, self._count)
        self.name = name

    def __call__(self, selections):
        self._apply_trills(selections)

    def _apply_trills(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vector = self.boolean_vector
        for tie, bool in zip(ties, vector(r=len(ties))):
            if bool is 1:
                if all(
                    isinstance(leaf, abjad.Chord)
                    for leaf in abjad.iterate(tie).leaves()
                ):
                    old_chord = tie[0]
                    base_pitch = old_chord.written_pitches[0]
                    trill_pitch = old_chord.written_pitches[-1]
                    new_leaf = abjad.Note(base_pitch, old_chord.written_duration)

                    trill_start = abjad.LilyPondLiteral(
                        r"\pitchedTrill", format_slot="before"
                    )
                    trill_literal = abjad.LilyPondLiteral(
                        fr"\startTrillSpan {trill_pitch}", format_slot="after"
                    )
                    trill_stop = abjad.LilyPondLiteral(
                        r"\stopTrillSpan", format_slot="after"
                    )
                    abjad.attach(trill_start, new_leaf)
                    abjad.attach(trill_literal, new_leaf)
                    last_leaf = tie[-1]
                    next_leaf = abjad.inspect(last_leaf).leaf(1)
                    if next_leaf is not None:
                        abjad.attach(trill_stop, next_leaf)
                    else:
                        continue
                    indicators = abjad.inspect(old_chord).indicators()
                    for indicator in indicators:
                        abjad.attach(indicator, new_leaf)

                    parent = abjad.inspect(old_chord).parentage().parent
                    parent[parent.index(old_chord)] = new_leaf

                    tail = abjad.select(tie).leaves()[1:]
                    for leaf in tail:
                        new_tail = abjad.Note(base_pitch, leaf.written_duration)
                        indicators = abjad.inspect(leaf).indicators()
                        for indicator in indicators:
                            abjad.attach(indicator, new_tail)
                        before_grace = abjad.inspect(leaf).before_grace_container()
                        if before_grace is not None:
                            abjad.attach(before_grace, new_tail)
                        parent = abjad.inspect(leaf).parentage().parent
                        parent[parent.index(leaf)] = new_tail
                else:
                    continue
            else:
                continue

    def name(self):
        return self.name

    def state(self):
        return f"""count\n{self.boolean_vector.state()}"""


# ###DEMO###
# staff = abjad.Staff("<c' d'>4 c'4 c'4 <c' d'>4 c'4 c'4 c'4 c'4 ")
# handler = TrillHandler(boolean_vector=[0, 0], continuous=True)
# handler(staff)
# abjad.f(staff)
