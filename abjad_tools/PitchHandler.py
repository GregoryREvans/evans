import abjad

class PitchHandler:

    def __init__(
        self,
        pitch_list=None,
        continuous=False,
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
        return self._apply_pitches(selections, self.pitch_list)

    def _collect_pitches_durations_leaves(self, logical_ties, pitches):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        cyc_pitches = cyc(pitches)
        pitches, durations, leaves = [[], [], []]
        for tie in logical_ties:
            if isinstance(tie[0], abjad.Note):
                pitch = next(cyc_pitches)
                for leaf in tie:
                    pitches.append(pitch)
                    durations.append(leaf.written_duration)
                    leaves.append(leaf)
            else:
                for leaf in tie:
                    pitches.append(None)
                    durations.append(leaf.written_duration)
                    leaves.append(leaf)
        return pitches, durations, leaves

    def _apply_pitches(self, selections, pitches):
        leaf_maker = abjad.LeafMaker()
        container = abjad.Container(selections)
        old_ties = [tie for tie in abjad.iterate(
            container).logical_ties()]
        pitches, durations, old_leaves = self._collect_pitches_durations_leaves(
            old_ties, pitches)
        new_leaves = [leaf for leaf in leaf_maker(pitches, durations)]
        for old_leaf, new_leaf in zip(old_leaves, new_leaves):
            indicators = abjad.inspect(old_leaf).indicators()
            for indicator in indicators:
                abjad.attach(indicator, new_leaf)
            parent = abjad.inspect(old_leaf).parentage().parent
            parent[parent.index(old_leaf)] = new_leaf
        return [container[:]]
