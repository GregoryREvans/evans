import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class PitchHandler:
    def __init__(self, pitch_list=None, continuous=False):
        self.pitch_list = pitch_list
        self.continuous = continuous
        self._count = -1

    def __call__(self, selections):
        return self._apply_pitches(selections)

    def _collect_pitches_durations_leaves(self, logical_ties, pitches):

        cyc_pitches = CyclicList(pitches, self.continuous, self._count)
        pitches, durations, leaves = [[], [], []]
        for tie in logical_ties:
            if isinstance(tie[0], abjad.Note):
                pitch = cyc_pitches(r=1)[0]
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

    def _apply_pitches(self, selections):
        pitches = self.pitch_list
        leaf_maker = abjad.LeafMaker()
        old_ties = [tie for tie in abjad.iterate(selections).logical_ties()]
        pitches, durations, old_leaves = self._collect_pitches_durations_leaves(
            old_ties, pitches
        )
        new_leaves = [leaf for leaf in leaf_maker(pitches, durations)]
        for old_leaf, new_leaf in zip(old_leaves, new_leaves):
            indicators = abjad.inspect(old_leaf).indicators()
            for indicator in indicators:
                abjad.attach(indicator, new_leaf)
            abjad.mutate(old_leaf).replace(new_leaf)
