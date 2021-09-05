import abjad
from abjadext import microtones


class HEJIAccidental:  # give a _tweaks value?
    def __init__(
        self,
        accidental_markup=None,
    ):
        self.accidental_markup = accidental_markup


class HEJIPitch:
    def __init__(
        self,
        fundamental=None,
        ratio=None,
    ):
        self.fundamental = fundamental
        self.ratio = ratio
        self.bundle = microtones.make_ji_bundle(self.fundamental, self.ratio)
        self.accidental = self._calculate_accidental_markup()
        self.et_cent_deviation_markup = self._calculate_et_cent_deviation()
        self.written_pitch = self._calculate_written_pitch()

    def __str__(self):
        s = f"{self.written_pitch}!"  # do not allow to be unforced?
        return s

    def _calculate_accidental_markup(self):
        accidental_markup = self.bundle.vector.calculate_ji_markup()
        a = HEJIAccidental(accidental_markup)
        return a

    def _calculate_et_cent_deviation(self):
        deviation = microtones.return_cent_deviation_markup(
            ratio=self.ratio,
            fundamental=self.fundamental,
            chris=False,
        )
        return deviation

    def _calculate_written_pitch(self):
        temp_note = abjad.Note(self.fundamental, (1, 4))
        microtones.tune_to_ratio(temp_note.note_head, self.ratio)
        written_pitch = temp_note.written_pitch
        return written_pitch

    def _get_lilypond_format(self):
        return str(self)


p = HEJIPitch("c'", "5/4")
print(p)
print(p.fundamental)
print(p.ratio)
print(p.accidental)
print(p.et_cent_deviation_markup)
print(p.written_pitch)
