import copy

import abjad


def adjacent_interval_inversion(iterable):
    out = []
    for i in range(len(iterable) - 1):
        leaf1 = iterable[i]
        leaf2 = iterable[i + 1]
        pitch1 = leaf1.written_pitch
        pitch2 = leaf2.written_pitch
        interval = abjad.NamedInterval.from_pitch_carriers(pitch1, pitch2)
        inverted_interval = abjad.NamedInterval("P1") - interval
        new_pitch = inverted_interval.transpose(leaf1.written_pitch)
        new_leaf = copy.copy(leaf1)
        new_leaf.written_pitch = new_pitch
        out.append(new_leaf)
    return out


staff1 = abjad.Staff(
    "a'8 f'8 d'8 a'8 f'8 d'8 d''8 bf'8 g'8 bf'8 g'8 e'8 g'8 e'8 cs'8 g'8 e'8 cs'8 a'8 f'8 d'8",
    name="first_staff",
)
new_leaves = adjacent_interval_inversion(staff1)
staff2 = abjad.Staff(new_leaves, name="second_staff")
score = abjad.Score(
    [abjad.StaffGroup([staff1, staff2], name="my_group")], name="my_score"
)
moment = abjad.SchemeMoment((1, 20))
abjad.setting(score).proportional_notation_duration = moment
file = abjad.LilyPondFile(
    items=[score],
    includes=["/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"],
    global_staff_size=16,
)
abjad.show(file)
abjad.play(score)
