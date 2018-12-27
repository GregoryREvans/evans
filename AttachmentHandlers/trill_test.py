import abjad

staff = abjad.Staff([abjad.Chord([0, 3], abjad.Duration(1, 4))])
for chord in abjad.select(staff).components(abjad.Chord):
    notes = abjad.inspect(chord).pitches()
    new_note = abjad.Note(notes[0])
    trill = abjad.TrillSpanner(pitch=abjad.NamedPitch(notes[-1]))
    abjad.attach(trill, new_note)
    print(new_note)


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


# abjad.show(staff)
