import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class PitchHandler:
    def __init__(
        self, pitch_list=None, continuous=False, count=-1, name="Pitch Handler"
    ):
        self.pitch_list = pitch_list
        self.continuous = continuous
        self.name = name
        self._count = count
        self._cyc_pitches = CyclicList(self.pitch_list, self.continuous, self._count)

    def __call__(self, selections):
        self._apply_pitches(selections)

    def _collect_pitches_durations_leaves(self, logical_ties):
        pitches, durations, leaves = [[], [], []]
        for tie in logical_ties:
            if isinstance(tie[0], abjad.Note):
                pitch = self._cyc_pitches(r=1)[0]
                for leaf in tie:
                    pitches.append(pitch)
                    durations.append(leaf.written_duration)
                    leaves.append(leaf)
            else:
                continue
        return pitches, durations, leaves

    def _apply_pitches(self, selections):
        leaf_maker = abjad.LeafMaker()
        old_ties = [
            tie
            for tie in abjad.iterate(selections).logical_ties()
            if isinstance(tie[0], abjad.Note)
        ]
        if len(old_ties) > 0:
            pitches, durations, old_leaves = self._collect_pitches_durations_leaves(
                old_ties
            )
            new_leaves = [leaf for leaf in leaf_maker(pitches, durations)]
            for old_leaf, new_leaf in zip(old_leaves, new_leaves):
                indicators = abjad.inspect(old_leaf).indicators()
                before_grace = abjad.inspect(old_leaf).before_grace_container()
                for indicator in indicators:
                    abjad.attach(indicator, new_leaf)
                if before_grace is not None:
                    abjad.attach(before_grace, new_leaf)
                abjad.mutate(old_leaf).replace(new_leaf)

    def name(self):
        return self.name

    def state(self):
        return f"""count\n{self._cyc_pitches.state()}"""

###DEMO
# s = abjad.Staff("c'4 c'4 c'4 c'4")
# grace = abjad.BeforeGraceContainer("c'16")
# abjad.attach(grace, s[1])
# handler = PitchHandler(
#     pitch_list=[0, 1, 2, 3, 4],
#     continuous=True,
# )
# handler(abjad.select(s).logical_ties())
# abjad.f(s)
