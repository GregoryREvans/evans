print('Beaming runs ...')
for voice in abjad.select(score).components(abjad.Voice):
    for run in abjad.select(voice).runs():
        if 1 < len(run):
            # use a beam_specifier to remove beam indicators from run
            specifier = abjadext.rmakers.BeamSpecifier(
                beam_each_division=False,
                )
            specifier(run)
        # for leaf in run:
        #     # continue if leaf can't be beamed
        #     if abjad.Duration(1, 4) <= leaf.written_duration:
        #         continue
        #     previous_leaf = abjad.inspect(leaf).leaf(-1)
        #     next_leaf = abjad.inspect(leaf).leaf(1)
        #     # if next leaf is quarter note (or greater) ...
        #     if (isinstance(next_leaf, (abjad.Chord, abjad.Note)) and
        #         abjad.Duration(1, 4) <= next_leaf.written_duration):
        #         left = previous_leaf.written_duration.flag_count
        #         right = leaf.written_duration.flag_count # right-pointing nib
        #         beam_count = abjad.BeamCount(
        #             left=left,
        #             right=right,
        #             )
        #         abjad.attach(beam_count, leaf)
        #         continue
        #     # if previous leaf is quarter note (or greater) ...
        #     if (isinstance(previous_leaf, (abjad.Chord, abjad.Note)) and
        #         abjad.Duration(1, 4) <= previous_leaf.written_duration):
        #         left = leaf.written_duration.flag_count # left-pointing nib
        #         right = next_leaf.written_duration.flag_count
        #         beam_count = abjad.BeamCount(
        #             left=left,
        #             right=right,
        #             )
        #         abjad.attach(beam_count, leaf)
            # then attach new indicators at the 0 and -1 of run
            #only on notes smaller than 1/4
    for note in abjad.select(voice).leaves(pitched=True):
        if abjad.inspect(note).duration() < abjad.Duration(1, 4):
            pre_leaf = abjad.inspect(note).leaf(-1)
            next_leaf = abjad.inspect(note).leaf(1)
            if isinstance(pre_leaf, abjad.Note):
                if abjad.inspect(pre_leaf).duration() >= abjad.Duration(1, 4):
                    abjad.attach(abjad.StartBeam(), note)
            if isinstance(pre_leaf, abjad.Rest):
                abjad.attach(abjad.StartBeam(), note)
            if pre_leaf == None:
                abjad.attach(abjad.StartBeam(), note)
            if isinstance(next_leaf, abjad.Note):
                if abjad.inspect(next_leaf).duration() >= abjad.Duration(1, 4):
                    abjad.attach(abjad.StopBeam(), note)
            if isinstance(next_leaf, abjad.Rest):
                abjad.attach(abjad.StopBeam(), note)
            if next_leaf == None:
                abjad.attach(abjad.StopBeam(), note)
