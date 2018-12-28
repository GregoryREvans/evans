import abjad

class TrillHandler:

    def __init__(
        self,
        pitch_list=None,
        continuous=True,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.pitch_list = pitch_list
        self.continuous = continuous
        self._cyc_pitches = cyc(pitch_list)
        self._count = 0

    def __call__(self, selections):
        return self._apply_trills(selections)

    def _collect_pitches_durations_leaves(self, logical_ties):
        pitches, trill_notes, durations, leaves = [[], [], [], []]
        for tie in logical_ties:
            if isinstance(tie[0], abjad.Chord):
                pitch = abjad.inspect(tie).logical_tie()
                for leaf in tie:
                    pitches.append(pitch[0])
                    trill_notes.append(pitch[-1])
                    durations.append(leaf.written_duration)
                    leaves.append(leaf)
            else:
                for leaf in tie:
                    pitches.append(None)
                    durations.append(leaf.written_duration)
                    leaves.append(leaf)
        return pitches, trill_notes, durations, leaves

    def _apply_trills(self, selections):
        leaf_maker = abjad.LeafMaker()
        chords = abjad.select(selections).components(abjad.Chord)
        container = abjad.Container(chords)
        old_chords = [chord for chord in abjad.iterate(container).components(abjad.Chord)]
        pitches, trill_notes, durations, old_chords = self._collect_pitches_durations_leaves(old_chords)
        new_trills = [leaf for leaf in leaf_maker(pitches, durations)]
        for new_trill, trill_note in zip(new_trills, trill_notes):
            trill = abjad.TrillSpanner(pitch=abjad.NamedPitch(trill_note))
            abjad.attach(trill, new_trill)
        for old_chord, new_trill in zip(old_chord, new_trill):
            indicators = abjad.inspect(old_chord).indicators()
            for indicator in indicators:
                abjad.attach(indicator, new_trill[:])
            parent = abjad.inspect(old_chord).parentage().parent
            parent[parent.index(old_chord)] = new_trill
        return [container[:]]
