import abjad


class TrillHandler:

    # def __init__(
    #     self,
    #     pitch_list=None,
    #     continuous=True,
    #     ):
    #     def cyc(lst):
    #         if self.continuous == False:
    #             self._count = 0
    #         while True:
    #             yield lst[self._count % len(lst)]
    #             self._count += 1
    #     self.pitch_list = pitch_list
    #     self.continuous = continuous
    #     self._cyc_pitches = cyc(pitch_list)
    #     self._count = 0

    def __call__(self, selections):
        return self._apply_trills(selections)

    def _apply_trills(self, selections):
        container = abjad.Container()
        container.append(selections)

        for tie in abjad.iterate(container).logical_ties(pitched=True):
            if all(
                isinstance(leaf, abjad.Chord) for leaf in abjad.iterate(tie).leaves()
            ):
                old_chord = tie[0]
                base_pitch = old_chord.written_pitches[0]
                trill_pitch = old_chord.written_pitches[-1]
                interval_ = abjad.NamedInterval().from_pitch_carriers(
                    base_pitch, trill_pitch
                )
                new_leaf = abjad.Note(base_pitch, old_chord.written_duration)

                trill_start = abjad.LilyPondLiteral(
                    r"\pitchedTrill", format_slot="before"
                )
                trill_literal = abjad.LilyPondLiteral(
                    f"\startTrillSpan {trill_pitch}", format_slot="after"
                )
                trill_stop = abjad.LilyPondLiteral(
                    r"\stopTrillSpan", format_slot="after"
                )
                abjad.attach(trill_start, new_leaf)
                abjad.attach(trill_literal, new_leaf)
                last_leaf = tie[-1]
                next_leaf = abjad.inspect(last_leaf).leaf(1)
                if next_leaf != None:
                    abjad.attach(trill_stop, next_leaf)

                indicators = abjad.inspect(old_chord).indicators()
                for indicator in indicators:
                    abjad.attach(indicator, new_leaf)

                parent = abjad.inspect(old_chord).parentage().parent
                parent[parent.index(old_chord)] = new_leaf

                tail = abjad.select(tie).leaves()[1:]
                for leaf in tail:
                    new_tail = abjad.Note(base_pitch, leaf.written_duration)
                    parent = abjad.inspect(leaf).parentage().parent
                    parent[parent.index(leaf)] = new_tail
                    indicators = abjad.inspect(leaf).indicators()
                    for indicator in indicators:
                        abjad.attach(indicator, new_tail)

        return container[:]
