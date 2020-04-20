import abjad
from fractions import Fraction


def mixed_number(fraction_pair=(288, 5)):
    fraction_pair = Fraction(fraction_pair)
    q = fraction_pair.numerator // fraction_pair.denominator
    r = Fraction((fraction_pair.numerator % fraction_pair.denominator) / fraction_pair.denominator).limit_denominator()
    return (q, (r.numerator, r.denominator))

def compare_speed(
    l_note=None,
    r_note=None,
    ):
    left_dur = abjad.inspect(l_note).duration()
    right_dur = abjad.inspect(r_note).duration()
    multiplier = left_dur / right_dur
    return multiplier

def calculate_metric_modulation(
    l_tempo=60,
    l_note=None,
    r_note=None,
    ):
    left_dur = abjad.inspect(l_note).duration()
    right_dur = abjad.inspect(r_note).duration()
    multiplier = right_dur / left_dur
    new_tempo = l_tempo * multiplier
    return new_tempo

def metric_modulation(
    metronome_mark=((1, 4), 60),
    left_note=(abjad.Note("c'8")),
    right_note=(abjad.Note("c'8.")),
    modulated_beat=(abjad.Note("c'4")),
    ):
    tempo_note = abjad.Note()
    tempo_note.written_duration = metronome_mark[0]
    left_speed_multiplier = compare_speed(
        l_note=tempo_note,
        r_note=left_note
        )
    left_speed = metronome_mark[1] * left_speed_multiplier
    modulation_speed = calculate_metric_modulation(
        l_tempo=left_speed,
        l_note=left_note,
        r_note=right_note,
        )
    returned_speed = float(modulation_speed * compare_speed(left_note, modulated_beat))
    if returned_speed % 1 == 0.0:
        return int(returned_speed)
    else:
        return mixed_number(fraction_pair=returned_speed)

###DEMO###
# print(
#     metric_modulation(
#         metronome_mark=((1, 4), 96),
#         left_note=(abjad.Tuplet(multiplier=(5, 3), components=[abjad.Note()])),
#         right_note=(abjad.Note("c'4")),
#         modulated_beat=(abjad.Note("c'4")),
#     )
# )
#
# print(
#     metric_modulation(
#         metronome_mark=((1, 4), 96),
#         left_note=(abjad.Note("c'4.")),
#         right_note=(abjad.Note("c'4")),
#         modulated_beat=(abjad.Note("c'4")),
#     )
# )
