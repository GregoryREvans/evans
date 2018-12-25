import abjad
import abjadext.rmakers

class BeamHandler:

    def __init__(
        self,
        style=None,
        ):
        self.style = style

    def __call__(self, selections):
        return self.add_beams(selections)

    def add_beams(self, selections):
        if self.style != None:
            runs = abjad.select(selections).runs()
            for run in runs:
                specifier = abjadext.rmakers.BeamSpecifier(beam_each_division=False,)
                specifier(run)
                if self.style == 'rests':
                    abjad.beam(voice[:], beam_lone_notes=False, beam_rests=True,)
                else:
                    abjad.beam(voice[:], beam_lone_notes=False, beam_rests=False,)
        return selections
