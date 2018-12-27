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
        abjad.beam(selections[:], beam_lone_notes=False, beam_rests=False,)
        return selections
