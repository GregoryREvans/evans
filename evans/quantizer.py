import abjad
from abjadext import nauert, rmakers

from .sequence import CyclicList

# dont forget to work on a subclass of the rhythm trees in sequence?


def split_duration(milisecond_duration, cuts):
    if isinstance(cuts, (tuple, list)):
        total = sum(cuts)
        fractional_cuts = [_ / total for _ in cuts]
        subdivisions = [milisecond_duration * cut for cut in fractional_cuts]
    else:
        subdivisions = [milisecond_duration / cuts for _ in range(cuts)]
    return subdivisions


def ties_to_milisecond_durations(selections):
    reference_duration = abjad.Duration(1, 4)
    units_per_minute = 60
    tempo = abjad.MetronomeMark(reference_duration, units_per_minute)
    ties = abjad.select.logical_ties(selections)
    durations = [abjad.get.duration(_) for _ in ties]

    milisecond_durations = []

    for dur in durations:
        result = dur / reference_duration / units_per_minute * 60
        dur = abjad.Duration(result)
        milisecond_durations.append(result * 1000)
    for i, tie in enumerate(ties):
        if isinstance(tie[0], abjad.Rest):
            milisecond_durations[i] = 1 - milisecond_durations[i]
    return milisecond_durations


def do_subdivide_durations(durations, cuts=[2], indices=[0], period=1, cyclic=True):
    counter = 0
    cyclic_subdivisions = CyclicList(cuts, forget=False)

    for i, duration in enumerate(durations):
        if duration < 0:
            continue
        if cyclic is False:
            period = indices[-1] + 1
            if indices[-1] < i:
                break
        if counter == period:
            counter = 0
        if counter in indices:
            relevant_number = cyclic_subdivisions(r=1)[0]
            parts = split_duration(duration, relevant_number)
            durations[i] = parts
        counter += 1

    flattened_sequence = abjad.sequence.flatten(durations)

    return flattened_sequence


def subdivide_durations(cuts=[2], indices=[0], period=1, cyclic=True):
    def returned_function(durations):
        subdivided_durations = do_subdivide_durations(
            durations, cuts=cuts, indices=indices, period=period, cyclic=cyclic
        )
        return subdivided_durations

    return returned_function


def do_fuse_durations(
    durations,
    group_sizes=[2],
    boolean_vector=[True],
    cyclic=True,
    overhang=False,
    reversed_=False,
):
    out = []
    partitions = abjad.sequence.partition_by_counts(
        durations,
        group_sizes,
        cyclic=cyclic,
        enchain=False,
        overhang=overhang,  # True, False, abjad.EXACT
        reversed_=reversed_,
    )
    if cyclic is True:
        cyclic_vector = CyclicList(boolean_vector, forget=False)
        for partition in partitions:
            boolean_value = cyclic_vector(r=1)[0]
            if boolean_value is True:
                out.append(sum(partition))
            else:
                out.append(partition)
    else:
        for i, pair in enumerate(zip(boolean_vector, partitions)):
            boolean_value, partition = pair
            if boolean_value is True:
                out.append(sum(partition))
            else:
                out.append(partition)
        if i < (len(partitions) - 1):
            out.append(partitions[i:])

    flattened_sequence = abjad.sequence.flatten(out)

    return flattened_sequence


def fuse_durations(
    group_sizes=[2], boolean_vector=[True], cyclic=True, overhang=False, reversed_=False
):
    def returned_function(durations):

        fused_durations = do_fuse_durations(
            durations,
            group_sizes=group_sizes,
            boolean_vector=boolean_vector,
            cyclic=cyclic,
            overhang=overhang,
            reversed_=reversed_,
        )
        return fused_durations

    return returned_function


class QSchemaTimeSignature:
    def __init__(
        self,
        index,
        time_signature,
        use_full_measure,
    ):
        self.index = index
        self.time_signature = time_signature
        self.use_full_measure = use_full_measure
        self.constructed_dict = (
            index,
            {
                "time_signature": abjad.TimeSignature(time_signature),
                "use_full_measure": use_full_measure,
            },
        )


def miliseconds_to_music(*args, miliseconds, fuse_silences=True, search_tree=None):

    schemas = [arg.constructed_dict for arg in args]

    seq = nauert.QEventSequence.from_millisecond_durations(
        miliseconds, fuse_silences=fuse_silences
    )

    if search_tree is None:
        print("NO SEARCH TREE")
        search_tree = nauert.UnweightedSearchTree(  # default
            definition={
                2: {
                    2: {2: {2: None}, 3: None},
                    3: None,
                    5: None,
                    7: None,
                },
                3: {
                    2: {2: None},
                    3: None,
                    5: None,
                },
                5: {
                    2: None,
                    3: None,
                },
                7: {2: None},
                11: None,
                13: None,
            }
        )
    else:
        print("GIVEN A SEARCH TREE")
        search_tree = nauert.UnweightedSearchTree(
            definition=search_tree
        )

    # search_tree = nauert.UnweightedSearchTree( # too complex
    #     definition={
    #         2: {
    #             2: {
    #                 2: None,
    #                 3: None,
    #                 5: None,
    #             },
    #             3: {
    #                 2: None,
    #             },
    #             5: {
    #                 2: None,
    #             },
    #             7: { # too deep?
    #                 2: None,
    #             },
    #         },
    #         3: {
    #             2: {
    #                 2: None,
    #                 3: None,
    #                 5: None,
    #             },
    #             3: {
    #                 2: None,
    #             },
    #             5: {
    #                 2: None,
    #             },
    #             7: { # too deep?
    #                 2: None,
    #             },
    #         },
    #         5: {
    #             2: {
    #                 2: None,
    #                 3: None,
    #                 5: None,
    #             },
    #             3: {
    #                 2: None,
    #             },
    #             5: {
    #                 2: None,
    #             },
    #         },
    #         7: {
    #             2: {
    #                 2: None,
    #                 3: None,
    #                 5: None,
    #             },
    #             3: {
    #                 2: None,
    #             },
    #         },
    #         11: {
    #             2: {
    #                 2: None,
    #                 3: None,
    #                 5: None,
    #             },
    #         },
    #         13: None,
    #     }
    # )

    q_schema = nauert.MeasurewiseQSchema(
        *schemas,
        tempo=abjad.MetronomeMark(abjad.Duration(1, 4), 60),
        search_tree=search_tree,
        use_full_measure=True,
    )

    result = nauert.quantize(
        seq,
        q_schema=q_schema,
        heuristic=nauert.DistanceHeuristic(),
        attack_point_optimizer=nauert.NaiveAttackPointOptimizer(),
        # attack_point_optimizer=nauert.MeasurewiseAttackPointOptimizer(),
        grace_handler=nauert.DiscardingGraceHandler(),
        attach_tempos=False,
    )
    # print(result, "\n")
    return result


def make_subdivided_music(*args, ties, search_tree=None):
    schemas = []
    ties = abjad.select.logical_ties(ties)
    milisecond_durations = ties_to_milisecond_durations(ties)

    for arg in args:
        if isinstance(arg, QSchemaTimeSignature):
            schemas.append(arg)
        else:
            milisecond_durations = arg(milisecond_durations)

    result = miliseconds_to_music(*schemas, miliseconds=milisecond_durations, search_tree=search_tree)
    # print(result, "\n")
    returned_result = abjad.mutate.eject_contents(result)
    # print(returned_result, "\n")
    return returned_result


# result = make_subdivided_music(
#     QSchemaTimeSignature(
#         index=0,
#         time_signature=abjad.TimeSignature((2, 4)),
#         use_full_measure=True,
#     ),
#     QSchemaTimeSignature(
#         index=1,
#         time_signature=abjad.TimeSignature((2, 4)),
#         use_full_measure=True,
#     ),
#     subdivide_durations(
#         cuts=[(4, 1), 2],
#         indices=[0, 1],
#         period=5,
#     ),
#     fuse_durations(
#         group_sizes=[2, 3],
#         boolean_vector=[True, False],
#         cyclic=True,
#         overhang=False,
#         reversed_=False,
#     ),
#     # subdivide_durations(
#     #     cuts=[2],
#     #     indices=[0],
#     #     period=1,
#     # ),
#     ties=abjad.select.logical_ties(s),
# )


def score_to_timespans(score):
    ties = abjad.select.logical_ties(score, pitched=True)
    spans = abjad.TimespanList([abjad.get.timespan(tie) for tie in ties])
    return spans


def fuse_timespanlist_preserving_start_offsets(spans, start_offsets_only=True):
    if start_offsets_only is True:
        start_offsets = [span.start_offset for span in spans]
        start_offsets.append(spans.stop_offset)
        start_offsets = list(set(start_offsets))
        start_offsets.sort()
        new_spans = []
        for start, stop in abjad.sequence.nwise(start_offsets, 2):
            new_spans.append(abjad.Timespan(start, stop))
        spans = new_spans
    offset_counter = abjad.OffsetCounter(spans)
    offsets = list(set(item[0] for item in offset_counter.items.items()))
    offsets.sort()
    reduced_spans = []
    for start, stop in abjad.sequence.nwise(offsets, 2):
        reduced_spans.append(abjad.Timespan(start, stop))
    final_tsl = abjad.TimespanList(reduced_spans)
    return final_tsl


def duration_to_milisecond_durations(durations):
    reference_duration = abjad.Duration(1, 4)
    units_per_minute = 60
    tempo = abjad.MetronomeMark(reference_duration, units_per_minute)

    milisecond_durations = []

    for dur in durations:
        result = dur / reference_duration / units_per_minute * 60
        milisecond_durations.append(result * 1000)

    return milisecond_durations


def truncate_list_of_durations(milisecond_durations, cap_milisecond):
    out = [0]
    abs_miliseconds = [abs(_) for _ in milisecond_durations]
    for duration in milisecond_durations:
        temp = [_ for _ in out]
        temp.append(duration)
        current_total = sum([abs(_) for _ in temp])
        if current_total < cap_milisecond:
            out.append(duration)
        else:
            difference = current_total - cap_milisecond
            if 0 < duration:
                new_dur = duration - difference
            else:
                new_dur = duration + difference
            temp[-1] = new_dur
            assert (
                sum([abs(_) for _ in temp]) == cap_milisecond
            ), f"out total:{sum([abs(_) for _ in temp])} vs desired total:{cap_milisecond}"
            out.append(new_dur)
            break
    out = out[1:]
    assert (
        sum([abs(_) for _ in out]) == cap_milisecond
    ), f"BAD TRUNCATION: out sum = {sum([abs(_) for _ in out])} vs cap milisecond {cap_milisecond}"
    return [abjad.Duration(_) for _ in out]


def unity_capsule_rhythms(
    *args,
    trailing_divisions,
    treat_tuplets=False,
    intercalate_silences_between_groups=False,
    rest_durations="divisions",  # or [(1, 4), (1, 8) ...]
    rest_boolean_vector=[True],
    cyclic_vector=True,
    group_sizes=[2],
    cyclic_groups=True,
    yield_silence_duration_per_application_site=False,
    show_illustrated_process=False,
):

    user_input_schemas = []
    for arg in args:
        if isinstance(arg, QSchemaTimeSignature):
            user_input_schemas.append(arg)

    def returned_function(
        divisions,
        rest_durations=rest_durations,
        rest_boolean_vector=rest_boolean_vector,
    ):
        if intercalate_silences_between_groups is True:
            if rest_durations == "divisions":
                rest_divisions = divisions
            else:
                rest_divisions = rest_durations
            rest_durations = [abjad.Duration(_) for _ in rest_divisions]
            rest_milisecond_durations = [
                0 - _ for _ in duration_to_milisecond_durations(rest_durations)
            ]
        represented_schema_indices = [_.index for _ in user_input_schemas]
        schema_list = user_input_schemas
        for i, division in enumerate(divisions):
            if i not in represented_schema_indices:
                schema = QSchemaTimeSignature(
                    index=i,
                    time_signature=division,
                    use_full_measure=True,
                )
                schema_list.append(schema)
        total_duration = sum([abjad.Duration(_) for _ in divisions])
        full_divisions = divisions + trailing_divisions
        pairs = [_ for _ in abjad.sequence.nwise(divisions, 2)]
        required_trails = []
        for i, division in enumerate(divisions):
            following_divisions = len(divisions) - i
            temp_trail = division.numerator - following_divisions
            if 0 < temp_trail:
                required_trails.append(temp_trail)
        required_trail_count = max(required_trails)
        assert (
            len(trailing_divisions) == required_trail_count
        ), f"required_trail_count: {required_trail_count} != trailing_divisions: {len(trailing_divisions)}"
        temp_staff_group = abjad.StaffGroup()
        counter = -1
        total_pairs = len(pairs)
        for pair in pairs:
            counter += 1
            if show_illustrated_process is True:
                print(f"Pair {counter} of {total_pairs}: {pair[0]}, {pair[1]}\n")
            staff_1 = abjad.Staff(lilypond_type="RhythmicStaff")
            staff_2 = abjad.Staff(lilypond_type="RhythmicStaff")
            if 0 < counter:
                preceding_silence_divisions = sum(
                    [abjad.Duration(_) for _ in full_divisions[0:counter]]
                )
                pause_1 = rmakers.multiplied_duration(
                    [preceding_silence_divisions], prototype=abjad.Skip
                )
                staff_1.append(pause_1[0])
                # rmakers.force_rest(staff_1)

                pause_2 = rmakers.multiplied_duration(
                    [preceding_silence_divisions], prototype=abjad.Skip
                )
                staff_2.append(pause_2[0])
                # rmakers.force_rest(staff_2)

            first_numerator = pair[0].numerator  # what about denominators?
            second_numerator = pair[1].numerator

            target_1 = sum(
                [
                    abjad.Duration(_)
                    for _ in full_divisions[counter : counter + second_numerator]
                ]
            )
            layer_1 = rmakers.tuplet([target_1], [(1 for _ in range(first_numerator))])
            staff_1.extend(layer_1)
            temp_staff_group.append(staff_1)

            target_2 = sum(
                [
                    abjad.Duration(_)
                    for _ in full_divisions[counter : counter + first_numerator]
                ]
            )
            layer_2 = rmakers.tuplet([target_2], [(1 for _ in range(second_numerator))])
            staff_2.extend(layer_2)
            temp_staff_group.append(staff_2)

        spans = score_to_timespans(temp_staff_group)
        fused_spans = fuse_timespanlist_preserving_start_offsets(spans)
        cutoff = abjad.Timespan(total_duration.pair, abjad.Infinity())
        clipped_spans = fused_spans - cutoff
        durations = [_.duration for _ in clipped_spans]
        milisecond_durations = duration_to_milisecond_durations(durations)
        if intercalate_silences_between_groups is True:
            groups = abjad.select.partition_by_counts(
                milisecond_durations, group_sizes, cyclic=cyclic_groups, overhang=True
            )
            cyclic_rests = CyclicList(rest_milisecond_durations, forget=False)
            yield_vector = CyclicList(rest_boolean_vector, forget=False)
            if cyclic_vector is True:
                rest_boolean_vector = yield_vector(r=len(groups))
            # yeild_silence_duration_per_application_site=False,
            interleaved_durations = []
            for i, group in enumerate(groups):
                if i < len(rest_boolean_vector):
                    current_bool = rest_boolean_vector[i]
                    if yield_silence_duration_per_application_site is True:
                        if current_bool is True:
                            group.extend(cyclic_rests(r=1))
                        else:
                            current_rest = cyclic_rests(r=1)
                            if current_bool is True:
                                group.extend(current_rest)
                interleaved_durations.extend(group)
            milisecond_durations = truncate_list_of_durations(
                interleaved_durations,
                duration_to_milisecond_durations([total_duration])[0],
            )
        milisecond_sum = abjad.Duration(
            sum([abs(_) / 1000 for _ in milisecond_durations])
        )
        total_duration_milisecond_sum = abjad.Duration(
            sum(
                [
                    abs(_) / 1000
                    for _ in duration_to_milisecond_durations([total_duration])
                ]
            )
        )
        assert (
            milisecond_sum == total_duration_milisecond_sum
        ), f"MILISECONDS MUST EQUAL MEASURES: miliseconds:{milisecond_sum} vs measures:{total_duration}"

        nested_music = miliseconds_to_music(
            *schema_list,
            miliseconds=milisecond_durations,
        )
        if show_illustrated_process is True:
            copied_music = abjad.mutate.copy(nested_music)
            final_staff = abjad.Staff(lilypond_type="RhythmicStaff")
            for component in copied_music:
                if isinstance(component, list):
                    final_staff.extend(component)
                else:
                    final_staff.append(component)
            for rest_group in abjad.select.group_by_contiguity(
                abjad.select.rests(temp_staff_group)
            ):
                start_literal = abjad.LilyPondLiteral(
                    [
                        r"\override Rest.transparent = ##t",
                        r"\override Dots.transparent = ##t",
                        r"\stopStaff \override Staff.StaffSymbol.line-count = 0 \startStaff",
                    ],
                    site="before",
                )
                stop_literal = abjad.LilyPondLiteral(
                    [
                        r"\override Dots.transparent = ##f",
                        r"\stopStaff \override Staff.StaffSymbol.line-count = 1 \startStaff",
                    ],
                    site="after",
                )
                abjad.attach(start_literal, rest_group[0])
                abjad.attach(stop_literal, rest_group[-1])
            duplicate_long_beam(
                final_staff, beam_rests=True, beam_lone_notes=False
            )
            temp_staff_group.append(final_staff)
            score = abjad.Score([temp_staff_group])
            file = abjad.LilyPondFile(
                items=[
                    r'#(set-default-paper-size "11x17landscape")',
                    r"#(set-global-staff-size 18)",
                    r'\include "/Users/gregoryevans/abjad/abjad/scm/abjad.ily"',
                    abjad.Block(
                        "layout",
                        items=[
                            r"""
                              	indent = 0
                                  ragged-bottom = ##t
                                  ragged-last = ##t
                                  ragged-right = ##t
                              	\context {
                              		\Score
                              		\remove Metronome_mark_engraver
                              		\remove Mark_engraver
                              		\remove Bar_number_engraver
                              		\override BarLine.bar-extent = #'(-2 . 2)
                              		\override BarLine.hair-thickness = 0.5
                              		\override BarLine.X-extent = #'(0 . 0)
                              		\override BarLine.thick-thickness = #8
                              		\override Beam.breakable = ##t
                              		\override Beam.damping = #+inf.0 % was 99
                              		\override Beam.concaveness = #10000 % just trying this out
                              		\override Beam.beam-thickness = #1.15 % just trying this out
                              		\override Beam.length-fraction = #1.84 % just trying this out
                              		\override NoteColumn.ignore-collision = ##t % can cause bad merging!
                              		\override PaperColumn.used = ##t % just trying this out
                              		\override SpacingSpanner.spacing-increment = 1.25
                              		\override SpacingSpanner.uniform-stretching = ##t % trevor
                              		\override Stem.stemlet-length = #1.66
                              		\override Tie.height-limit = 6 % experimental
                              		\override Tie.thickness = 1.5 % experimental
                              		\override TupletBracket.breakable = ##t
                                      \override TupletBracket.full-length-to-extent = ##t
                                      \override TupletNumber.font-size = 1 % was 0.5
                              		\override TupletBracket.bracket-visibility = ##t
                              		\override TupletNumber.text = #tuplet-number::calc-fraction-text
                                      \override TupletNumber.layer = 11
                                      \override TupletNumber.whiteout = ##t
                              		\override TupletBracket.stencil = % just trying this out
                              		  #(lambda (grob)
                              			 (let* ((pos (ly:grob-property grob 'positions))
                              					(dir (ly:grob-property grob 'direction))
                              					(new-pos (if (= dir 1)
                              								 (max (car pos)(cdr pos))
                              								 (min (car pos)(cdr pos)))))
                              			   (ly:grob-set-property! grob 'positions (cons new-pos new-pos))
                              			   (ly:tuplet-bracket::print grob)))
                              		autoBeaming = ##f
                              		tupletFullLength = ##t
                                      \override TupletBracket.edge-text = #(cons
                                          (markup #:arrow-head X LEFT #f)
                                          (markup #:arrow-head X RIGHT #f)
                                      )
                                      proportionalNotationDuration = #(ly:make-moment 1 30)

                              	}
                                \context {
                              		\Voice
                              		\remove Forbid_line_break_engraver
                              	}
                              	\context {
                              		\StaffGroup
                                    \RemoveAllEmptyStaves
                              	}
                                  \context {
                                      \RhythmicStaff
                                    \override Beam.breakable = ##t
                              		fontSize = #-1
                                    \RemoveAllEmptyStaves
                                  }
                            """
                        ],
                    ),
                    abjad.Block("score", items=[score]),
                ],
            )
            raise Exception(abjad.show(file))
        for leaf in abjad.select.leaves(nested_music):
            signature_indicator = abjad.get.indicator(leaf, abjad.TimeSignature)
            abjad.detach(signature_indicator, leaf)
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if treat_tuplets is True:  # not needed?
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        music = abjad.mutate.eject_contents(container)
        assert sum(
            [abjad.get.duration(_) for _ in abjad.select.logical_ties(music)]
        ) == sum([abjad.Duration(_) for _ in divisions])
        return music

    return returned_function


def duplicate_long_beam(
    selections,
    stemlet_length=None,
    beam_rests=True,
    beam_lone_notes=False,
    direction=abjad.UP,
):  # because of circular import
    def less_than_quarter(leaf):
        if leaf.written_duration < abjad.Duration(1, 4):
            return True
        else:
            return False

    def get_beam_count(leaf):
        def _is_prime(n):
            if n == 1:
                return False
            if n % 2 == 0:
                return False
            i = 3
            while i * i <= n:
                if n % i == 0:
                    return False
                i += 2
            return True

        def _prime_factors(n):
            prime_factor_list = []
            while not n % 2:
                prime_factor_list.append(2)
                n //= 2
            while not n % 3:
                prime_factor_list.append(3)
                n //= 3
            i = 5
            while n != 1:
                if _is_prime(i):
                    while not n % i:
                        prime_factor_list.append(i)
                        n //= i
                i += 2
            return prime_factor_list

        duration = leaf.written_duration
        denominator = duration.denominator
        factors = _prime_factors(denominator)
        if len(factors) < 3:
            return 0
        else:
            factors = factors[2:]
            return len(factors)

    leaves = abjad.select.leaves(selections, grace=False)
    filtered_leaves = abjad.select.filter(leaves, less_than_quarter)
    groups = abjad.select.group_by_contiguity(filtered_leaves)
    for i, group in enumerate(groups):
        if len(groups) == 0:
            return
        if len(groups) == 1:
            abjad.beam(
                group,
                stemlet_length=stemlet_length,
                beam_lone_notes=beam_lone_notes,
                beam_rests=beam_rests,
            )
        if 1 < len(groups):
            total = len(groups) - 1
            first_leaf = group[0]
            last_leaf = group[-1]
            abjad.beam(
                group,
                stemlet_length=stemlet_length,
                beam_lone_notes=beam_lone_notes,
                beam_rests=beam_rests,
                direction=direction,
            )
            if i != 0:
                if i != total:
                    start_count = get_beam_count(first_leaf)
                    start_beam_count = abjad.BeamCount(
                        left=start_count, right=start_count
                    )
                    abjad.attach(start_beam_count, first_leaf)
                    stop_count = get_beam_count(last_leaf)
                    stop_beam_count = abjad.BeamCount(right=stop_count, left=stop_count)
                    abjad.attach(stop_beam_count, last_leaf)
            if i == 0:
                stop_count = get_beam_count(last_leaf)
                stop_beam_count = abjad.BeamCount(right=stop_count, left=stop_count)
                abjad.attach(stop_beam_count, last_leaf)
            if i == total:
                start_count = get_beam_count(first_leaf)
                start_beam_count = abjad.BeamCount(left=start_count, right=start_count)
                abjad.attach(start_beam_count, first_leaf)
