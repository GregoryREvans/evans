for voice in abjad.select(score).components(abjad.Voice):
    for run in abjad.select(voice).runs():
        specifier = abjadext.rmakers.BeamSpecifier(
            beam_each_division=False,
            )
        specifier(run)
    abjad.beam(voice[:], beam_lone_notes=False, beam_rests=False,)
