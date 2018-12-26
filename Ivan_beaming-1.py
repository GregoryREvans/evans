
for voice in abjad.select(score).components(abjad.Voice):
    for run in abjad.select(voice).runs():
        # use a beam_specifier to remove beam indicators from run
        specifier = abjadext.rmakers.BeamSpecifier(
            beam_each_division=False,
            )
        specifier(run)
    for leaf in abjad.select(voice).leaves():
        if leaf.written_duration <= abjad.Duration(7, 32):
            previous_leaf = abjad.inspect(leaf).leaf(-1)
            next_leaf = abjad.inspect(leaf).leaf(1)
            prev_dur = 100
            next_dur = 100
            if hasattr(previous_leaf, 'written_duration'):
                prev_dur = previous_leaf.written_duration
            if hasattr(next_leaf, 'written_duration'):
                next_dur = next_leaf.written_duration

            if all(dur >= abjad.Duration(1, 4) for dur in (prev_dur, next_dur)) \
            or all(isinstance(l, abjad.Rest) for l in (previous_leaf, next_leaf)):
                continue 
            if prev_dur >= abjad.Duration(1, 4) or isinstance(previous_leaf, abjad.Rest):
                abjad.attach(abjad.StartBeam(), leaf)
            if next_dur >= abjad.Duration(1, 4) or isinstance(next_leaf, abjad.Rest):
                abjad.attach(abjad.StopBeam(), leaf)