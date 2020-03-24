import abjad


def beam_meter(components, meter, offset_depth, include_rests=True):
    offsets = meter.depthwise_offset_inventory[offset_depth]
    offset_pairs = []
    for i, _ in enumerate(offsets[:-1]):
        offset_pair = [offsets[i], offsets[i + 1]]
        offset_pairs.append(offset_pair)
    initial_offset = abjad.inspect(components[0]).timespan().start_offset
    for i, pair in enumerate(offset_pairs):
        for i_, item in enumerate(pair):
            offset_pairs[i][i_] = item + initial_offset
    offset_timespans = [
        abjad.timespan(start_offset=pair[0], stop_offset=pair[1])
        for pair in offset_pairs
    ]

    tup_list = [tup for tup in abjad.select(components).components(abjad.Tuplet)]
    for t in tup_list:
        if (
            isinstance(abjad.inspect(t).parentage().components[1], abjad.Tuplet)
            is False
        ):
            abjad.beam(
                t[:],
                beam_rests=include_rests,
                stemlet_length=0.75,
                beam_lone_notes=False,
                selector=abjad.select().leaves(grace=False)
            )
        else:
            continue

    non_tup_list = []
    for leaf in abjad.select(components).leaves():
        if (
            isinstance(abjad.inspect(leaf).parentage().components[1], abjad.Tuplet)
            is False
        ):
            non_tup_list.append(leaf)

    beamed_groups = []
    for i in enumerate(offset_timespans):
        beamed_groups.append([])

    for i, span in enumerate(offset_timespans):
        for group in (
            abjad.select(non_tup_list[:])
            .leaves()
            .group_by(
                predicate=lambda x: abjad.inspect(x)
                .timespan()
                .happens_during_timespan(span)
            )
        ):
            if abjad.inspect(group).timespan().happens_during_timespan(span) is True:
                beamed_groups[i].append(group[:])

    for subgroup in beamed_groups:
        subgrouper = abjad.select(subgroup).group_by_contiguity()
        for beam_group in subgrouper:
            # if not all(isinstance(leaf, abjad.Rest) for leaf in beam_group)
            abjad.beam(
                beam_group[:],
                beam_rests=include_rests,
                stemlet_length=0.75,
                beam_lone_notes=False,
                selector=abjad.select().leaves(grace=False)
            )

# ###DEMO###
# pre_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
# tuplet = abjad.Tuplet((2, 3), "c'8 r8 c'8")
# post_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
# staff = abjad.Staff()
# for _ in [pre_tuplet_notes[:], tuplet, post_tuplet_notes[:]]:
#     staff.append(_)
# beam_meter(components=staff[:], meter=abjad.Meter((4, 4)), offset_depth=1)
# abjad.show(staff)
