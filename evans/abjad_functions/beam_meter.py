import abjad


def beam_meter(
    components,
    meter,
    offset_depth,
    ):
    offsets = meter.depthwise_offset_inventory[offset_depth]
    offset_pairs = []
    for i, _ in enumerate(offsets[:-1]):
        offset_pair = [offsets[i], offsets[i + 1]]
        offset_pairs.append(offset_pair)
    initial_offset = abjad.inspect(components[0]).timespan().start_offset
    for i, pair in enumerate(offset_pairs):
        for i_, item in enumerate(pair):
            offset_pairs[i][i_] = item + initial_offset
    offset_timespans = [abjad.timespan(start_offset=pair[0], stop_offset=pair[1]) for pair in offset_pairs]

    beamed_groups = []
    for i in enumerate(offset_timespans):
        beamed_groups.append([])

    for i, span in enumerate(offset_timespans):
        for group in (
            abjad.select(components)
            .logical_ties()
            .group_by(
                predicate=lambda x: abjad.inspect(x)
                .timespan()
                .happens_during_timespan(span)
            )
        ):
            if (
                abjad.inspect(group).timespan().happens_during_timespan(span) is True
            ):
                beamed_groups[i].append(group[:])

    for group in beamed_groups:
        subgroups = []
        non_tuplets = []
        subgrouper = abjad.select(group).map(abjad.select())
        for item in subgrouper:
            if len(item) > 0:
                if abjad.inspect(item[0][0]).parentage().parent is abjad.Tuplet:
                    subgroups.append([item[:]])
                else:
                    non_tuplets.append(item[:])
        for subgroup in abjad.select(non_tuplets).group_by_contiguity():
            subgroups.append([subgroup[:]])
        for subgroup in subgroups:
            abjad.beam(subgroup[:])
            # if abjad.inspect(subgroup[0][0]).parentage().parent is not abjad.Tuplet:
            #     abjad.beam(subgroup[:])
            # else:
            #     beam_meter(subgroup[:])

###DEMO###
pre_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
post_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
staff = abjad.Staff()
for _ in [pre_tuplet_notes[:], tuplet, post_tuplet_notes[:]]:
    staff.append(_)
beam_meter(components=staff[:], meter=abjad.Meter((4, 4)), offset_depth=1)
abjad.f(staff)
