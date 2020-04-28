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
        met = abjad.MetronomeMark.make_tempo_equation_markup(
            abjad.inspect(modulated_beat).duration(),
            int(returned_speed),
        )
        mod =  abjad.MetricModulation(
            left_rhythm=left_note,
            right_rhythm=right_note,
            scale=(0.6, 0.6),
        )
        mark = abjad.LilyPondLiteral(
            [
                r"^ \markup {",
                r"  \huge",
                r"  \concat {",
                f"      {str(met)[8:]}",
                r"      \hspace #1",
                r"      \upright [",
                f"      {str(mod)[8:]}",
                r"      \hspace #0.5",
                r"      \upright ]",
                r"  }",
                r"}",
            ],
            format_slot="after",
        )
        return mark
    else:
        met = abjad.MetronomeMark.make_tempo_equation_markup(
            abjad.inspect(modulated_beat).duration(),
            Fraction(returned_speed).limit_denominator(),
        )
        mod =  abjad.MetricModulation(
            left_rhythm=left_note,
            right_rhythm=right_note,
            scale=(0.6, 0.6),
        )
        mark = abjad.LilyPondLiteral(
            [
                r"^ \markup {",
                r"  \huge",
                r"  \concat {",
                f"      {str(met)[8:]}",
                r"      \hspace #1",
                r"      \upright [",
                f"      {str(mod)[8:]}",
                r"      \hspace #0.5",
                r"      \upright ]",
                r"  }",
                r"}",
            ],
            format_slot="after",
        )
        return mark

###DEMO 1###
# m = metric_modulation(
#     metronome_mark=((1, 4), 96),
#     left_note=(abjad.Tuplet(multiplier=(5, 3), components=[abjad.Note()])),
#     right_note=(abjad.Note("c'4")),
#     modulated_beat=(abjad.Note("c'4")),
# )
# staff = abjad.Staff("c'1")
# abjad.attach(m, staff[0])
# abjad.f(staff)
###DEMO 2###
# m = metric_modulation(
#     metronome_mark=((1, 4), 96),
#     left_note=(abjad.Note("c'4.")),
#     right_note=(abjad.Note("c'4")),
#     modulated_beat=(abjad.Note("c'4")),
# )
# staff = abjad.Staff("c'1")
# abjad.attach(m, staff[0])
# abjad.f(staff)
###DEMO 3###
# m = metric_modulation(
#     metronome_mark=((1, 4), 71),
#     left_note=(abjad.Tuplet(multiplier=(10, 9), components=[abjad.Note("c'16")])),
#     right_note=(abjad.Note("c'16")),
#     modulated_beat=(abjad.Note("c'4")),
# )
# staff = abjad.Staff("c'1")
# abjad.attach(m, staff[0])
# abjad.f(staff)
###DEMO 4###
# m = metric_modulation(
#     metronome_mark=((1, 4), 40),
#     left_note=(abjad.Tuplet(multiplier=(2, 3), components=[abjad.Note("c'2")])),
#     right_note=(abjad.Note("c'2")),
#     modulated_beat=(abjad.Note("c'4")),
# )
# staff = abjad.Staff("c'1")
# abjad.attach(m, staff[0])
# abjad.f(staff)
