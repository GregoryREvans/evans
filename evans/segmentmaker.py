"""
SegmentMaker with supporting classes and functions.
"""
import datetime
import itertools
import os
import pathlib

import abjad
import black
import quicktions

from . import consort
from .commands import HandlerCommand, MusicCommand, RhythmCommand
from .handlers import PitchHandler
from .sequence import Sequence, flatten


class NoteheadBracketMaker:
    r"""
    Writes tuplet brackets with inserted note head.

    .. container:: example

        >>> tuplet = abjad.Tuplet((3, 2), "cs'8 d'8")
        >>> tuplet_2 = abjad.Tuplet((2, 3), components=[abjad.Note(0, (3, 8)), tuplet])
        >>> staff = abjad.Staff()
        >>> staff.append(tuplet_2)
        >>> staff.extend([abjad.Note("c'4"), abjad.Note("cs'8"), abjad.Note("d'8")])
        >>> new_brackets = evans.NoteheadBracketMaker()
        >>> new_brackets(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/abjad/scm/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \tweak TupletNumber.text #(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text 3 2) (ly:make-duration 2 0))
                \times 2/3
                {
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \tweak TupletNumber.text #(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text 2 3) (ly:make-duration 3 0))
                    \times 3/2
                    {
                        cs'8
                        d'8
                    }
                }
                c'4
                cs'8
                d'8
            }

    """

    def __call__(self, selections):
        return self._transform_brackets(selections)

    def __str__(self):
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        return f"<{type(self).__name__}()>"

    def _assemble_notehead(self, head_dur):
        duration_map = {
            "1": "0",
            "2": "1",
            "4": "2",
            "8": "3",
            "16": "4",
            "32": "5",
            "64": "6",
            "128": "7",
        }
        pair = head_dur.pair
        dot_parts = []
        while 1 < pair[0]:
            dot_part = (1, pair[1])
            dot_parts.append(dot_part)
            head_dur -= abjad.Duration(dot_part)
            pair = head_dur.pair
        duration_string = duration_map[f"{pair[1]}"]
        dot_string = ""
        for _ in dot_parts:
            dot_string += "."

        return duration_string, len(dot_string)

    def _transform_brackets(self, selections):
        for tuplet in abjad.select.tuplets(selections):
            rests = abjad.select.rests(tuplet)
            for rest_group in abjad.select.group_by_contiguity(rests):
                abjad.mutate.fuse(rest_group)
            inner_durs = []
            for _ in tuplet[:]:
                if isinstance(_, abjad.Tuplet):
                    inner_durs.append(_.multiplied_duration)
                else:
                    inner_durs.append(_.written_duration)
            tuplet_dur = sum(inner_durs)
            imp_num, imp_den = tuplet.implied_prolation.pair
            head_dur = tuplet_dur / imp_den
            dur_pair = self._assemble_notehead(head_dur)
            abjad.tweak(
                tuplet,
                rf"\tweak TupletNumber.text #(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text {imp_den} {imp_num}) (ly:make-duration {dur_pair[0]} {dur_pair[1]}))",
            )


class SegmentMaker:

    beaming = False

    def __init__(
        self,
        abbreviations=None,
        add_final_grand_pause=True,
        barline="||",
        beam_pattern="runs",
        beam_rests=False,
        clef_handlers=None,
        colophon=None,
        commands=None,
        current_directory=None,
        cutaway=True,
        fermata="scripts.ushortfermata",
        fermata_measures=None,
        instruments=None,
        names=None,
        name_staves=True,
        mm_rests=True,
        page_break_counts=None,
        rehearsal_mark=None,
        score_includes=None,
        score_template=None,
        segment_name=None,
        tempo=None,
        time_signatures=None,
        transpose_from_sounding_pitch=None,
        transparent_fermatas=True,
        tuplet_bracket_noteheads=True,
        with_layout=False,
        extra_rewrite=False,
    ):
        self.abbreviations = abbreviations
        self.add_final_grand_pause = add_final_grand_pause
        self.barline = barline
        self.beam_pattern = beam_pattern
        SegmentMaker.beaming = beam_rests
        self.clef_handlers = clef_handlers
        self.colophon = colophon
        self.commands = commands
        self.current_directory = current_directory
        self.cutaway = cutaway
        self.fermata = fermata
        self.fermata_measures = fermata_measures
        self.instruments = instruments
        self.names = names
        self.name_staves = name_staves
        self.mm_rests = mm_rests
        self.page_break_counts = page_break_counts
        self.rehearsal_mark = rehearsal_mark
        self.score_includes = score_includes
        self.score_template = score_template
        self.segment_name = segment_name
        self.tempo = tempo
        self.time_signatures = time_signatures
        self.transpose_from_sounding_pitch = transpose_from_sounding_pitch
        self.transparent_fermatas = transparent_fermatas
        self.tuplet_bracket_noteheads = tuplet_bracket_noteheads
        self.with_layout = with_layout
        self.extra_rewrite = extra_rewrite

    def __str__(self):
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        return f"<{type(self).__name__}()>"

    def _add_attachments(self):
        print("Adding attachments ...")
        if self.colophon is not None:
            last_voice = abjad.select.components(self.score_template, abjad.Voice)[
                -1
            ]  #
            colophon_leaf = abjad.select.leaves(last_voice)[-2]  #
            abjad.attach(self.colophon, colophon_leaf)

        if self.abbreviations is not None:
            abbreviations = []
            abb = self.abbreviations
            mark_abbreviations = [
                abjad.Markup(rf"\markup {{ \hcenter-in #12 {_} }}") for _ in abb
            ]
            for x in mark_abbreviations:
                abbreviations.append(abjad.ShortInstrumentName(markup=x))
        else:
            abbreviations = [_ for _ in range(len(self.instruments))]
        if self.names is not None:
            names = []
            nm = self.names
            mark_names = [
                abjad.Markup(rf"\markup {{ \hcenter-in #14 {_} }}") for _ in nm
            ]
            for x in mark_names:
                names.append(abjad.InstrumentName(markup=x))
        else:
            names = [_ for _ in range(len(self.instruments))]

        # metro = abjad.MetronomeMark(custom_markup=metro.make_tempo_equation_markup())#remove if broken
        if self.tempo is not None:
            metro = abjad.MetronomeMark(self.tempo[0], self.tempo[1])
            for staff in abjad.iterate.components(
                self.score_template["Global Context"],
                abjad.Staff,
            ):
                leaf1 = abjad.select.leaves(staff)[0]
                abjad.attach(metro, leaf1)

        markup2 = abjad.RehearsalMark(
            markup=abjad.Markup(rf"\markup \bold {{ {self.rehearsal_mark} }}")
        )
        if self.rehearsal_mark is not None:
            for staff in abjad.iterate.components(
                self.score_template["Global Context"],
                abjad.Staff,
            ):
                leaf1 = abjad.select.leaves(staff)[0]
                abjad.attach(markup2, leaf1)

        if self.barline is not None:
            bar_line = abjad.BarLine(self.barline)
            for voice in abjad.iterate.components(
                self.score_template["Staff Group"], abjad.Staff
            ):
                if self.barline == "|.":
                    last_leaf = abjad.select.leaves(voice)[-1]
                    abjad.attach(bar_line, last_leaf)
                else:
                    last_leaf = abjad.select.leaves(voice)[-3]
                    abjad.attach(bar_line, last_leaf)

        if self.clef_handlers is None:
            self.clef_handlers = [
                None
                for _ in abjad.select.components(
                    self.score_template["Staff Group"], abjad.Staff
                )
            ]
        for abbrev, name, inst, handler, voice in zip(
            abbreviations,
            names,
            self.instruments,
            self.clef_handlers,
            abjad.select.components(
                self.score_template["Staff Group"], abjad.Staff
            ),  # was Voice
        ):
            first_leaf = abjad.select.leaves(voice)[0]
            if self.name_staves is True:
                if not isinstance(abbrev, int):
                    abjad.attach(
                        abbrev,
                        first_leaf,
                        tag=abjad.Tag("applying staff names and clefs"),
                    )
                if not isinstance(name, int):
                    abjad.attach(
                        name,
                        first_leaf,
                        tag=abjad.Tag("applying staff names and clefs"),
                    )
            abjad.attach(
                inst, first_leaf, tag=abjad.Tag("applying staff names and clefs")
            )
            rhythm_commands_booleans = []
            for c in self.commands:
                if isinstance(c, RhythmCommand):
                    rhythm_commands_booleans.append(True)
                else:
                    rhythm_commands_booleans.append(False)
            if not any(rhythm_commands_booleans):
                out_of_range_pitches = abjad.iterpitches.iterate_out_of_range(voice)
                for leaf in out_of_range_pitches:
                    out_of_range_color = abjad.LilyPondLiteral(
                        r"\evans-pitch-out-of-range-coloring"
                    )
                    abjad.attach(
                        out_of_range_color,
                        leaf,
                        tag=abjad.Tag("PITCH"),
                        deactivate=False,
                    )
                # for leaf in abjad.select.leaves(voice, pitched=True): # remove?
                #     pitched_annotation = abjad.get.annotation(leaf, "pitched")
                #     if pitched_annotation is None:
                #         unpitch_color = abjad.LilyPondLiteral(
                #             r"\evans-not-yet-pitched-coloring"
                #         )
                #         abjad.attach(
                #             unpitch_color,
                #             leaf,
                #             tag=abjad.Tag("PITCH"),
                #             deactivate=False,
                #         )
            if self.transpose_from_sounding_pitch is True:
                abjad.iterpitches.transpose_from_sounding_pitch(voice)
            if handler is not None:
                handler(voice)

    def _add_ending_skips(self):
        print("Adding ending skips ...")
        last_skip = abjad.select.leaves(self.score_template["Global Context"])[-1]
        override_command = abjad.LilyPondLiteral(
            r"\once \override Score.TimeSignature.stencil = ##f", site="before"
        )
        abjad.attach(
            override_command, last_skip, tag=abjad.Tag("applying ending skips")
        )

        for voice in abjad.select.components(
            self.score_template["Staff Group"], abjad.Voice
        ):
            container = abjad.Container()
            sig = self.time_signatures[-1]
            leaf_duration = sig.duration / 2
            rest_leaf = abjad.Rest(1, multiplier=(leaf_duration))
            mult_rest_leaf = abjad.MultimeasureRest(1, multiplier=(leaf_duration))
            container.append(rest_leaf)
            container.append(mult_rest_leaf)
            markup = abjad.Markup(
                rf"""\markup \center-align \musicglyph #"{self.fermata}" """,
            )
            start_command = abjad.LilyPondLiteral(
                r"\stopStaff \once \override Staff.StaffSymbol.line-count = #0 \startStaff",
                site="before",
            )
            stop_command = abjad.LilyPondLiteral(
                r"\stopStaff \startStaff", site="after"
            )
            rest_literal = abjad.LilyPondLiteral(
                r"\once \override Rest.transparent = ##t", "before"
            )
            mult_rest_literal = abjad.LilyPondLiteral(
                r"\once \override MultiMeasureRest.transparent = ##t", "before"
            )
            penultimate_rest = container[0]
            final_rest = container[-1]
            abjad.attach(
                markup,
                final_rest,
                tag=abjad.Tag("applying ending skips"),
                direction=abjad.UP,
            )
            abjad.attach(
                start_command, penultimate_rest, tag=abjad.Tag("applying ending skips")
            )
            if self.barline == "|.":
                stop_command = abjad.LilyPondLiteral(r"\stopStaff", site="after")
                abjad.attach(
                    stop_command, final_rest, tag=abjad.Tag("applying ending skips")
                )
            else:
                abjad.attach(
                    stop_command, final_rest, tag=abjad.Tag("applying ending skips")
                )
            abjad.attach(
                rest_literal, penultimate_rest, tag=abjad.Tag("applying ending skips")
            )
            abjad.attach(
                mult_rest_literal, final_rest, tag=abjad.Tag("applying ending skips")
            )
            voice.extend(container[:])

    def beam_score(target):
        global_skips = [_ for _ in abjad.select.leaves(target["Global Context"])]
        sigs = []
        for skip in global_skips:
            for indicator in abjad.get.indicators(skip):
                if isinstance(indicator, abjad.TimeSignature):
                    sigs.append(indicator)
        print("Beaming meter ...")
        for voice in abjad.iterate.components(target["Staff Group"], abjad.Voice):
            for i, shard in enumerate(abjad.mutate.split(voice[:], sigs)):
                met = abjad.Meter(sigs[i].pair)
                inventories = [
                    x
                    for x in enumerate(
                        abjad.Meter(sigs[i].pair).depthwise_offset_inventory
                    )
                ]
                if sigs[i].denominator == 4:
                    beam_meter(
                        components=shard[:],
                        meter=met,
                        offset_depth=inventories[-1][0],
                        include_rests=SegmentMaker.beaming,
                        # include_rests=False,
                    )
                else:
                    beam_meter(
                        components=shard[:],
                        meter=met,
                        offset_depth=inventories[-2][0],
                        include_rests=SegmentMaker.beaming,
                        # include_rests=False,
                    )
        for trem in abjad.select.components(target, abjad.TremoloContainer):
            if abjad.StartBeam() in abjad.get.indicators(trem[0]):
                abjad.detach(abjad.StartBeam(), trem[0])
            if abjad.StopBeam() in abjad.get.indicators(trem[-1]):
                abjad.detach(abjad.StopBeam(), trem[-1])

    def beam_score_without_splitting(target):
        global_skips = [_ for _ in abjad.select.leaves(target["Global Context"])]
        sigs = []
        for skip in global_skips:
            for indicator in abjad.get.indicators(skip):
                if isinstance(indicator, abjad.TimeSignature):
                    sigs.append(indicator)
        print("Beaming meter ...")
        for voice in abjad.iterate.components(target["Staff Group"], abjad.Voice):
            leaves = abjad.select.leaves(voice[:])
            measures = abjad.select.group_by_measure(leaves)
            for i, shard in enumerate(measures):
                top_level_components = get_top_level_components_from_leaves(shard)
                shard = top_level_components  # WARNING: was originally wrapped in a selection
                met = abjad.Meter(sigs[i].pair)
                inventories = [
                    x
                    for x in enumerate(
                        abjad.Meter(sigs[i].pair).depthwise_offset_inventory
                    )
                ]
                if sigs[i].denominator == 4:
                    beam_meter(
                        components=shard[:],
                        meter=met,
                        offset_depth=inventories[-1][0],
                        include_rests=SegmentMaker.beaming,
                        # include_rests=False,
                    )
                else:
                    beam_meter(
                        components=shard[:],
                        meter=met,
                        offset_depth=inventories[-2][0],
                        include_rests=SegmentMaker.beaming,
                        # include_rests=False,
                    )
        for trem in abjad.select.components(target, abjad.TremoloContainer):
            if abjad.StartBeam() in abjad.get.indicators(trem[0]):
                abjad.detach(abjad.StartBeam(), trem[0])
            if abjad.StopBeam() in abjad.get.indicators(trem[-1]):
                abjad.detach(abjad.StopBeam(), trem[-1])

    def _break_pages(self):
        print("Breaking pages ...")
        if self.page_break_counts is not None:
            lit = abjad.LilyPondLiteral(r"\pageBreak", site="absolute_after")
            result = abjad.select.components(
                self.score_template["Global Context"], abjad.Skip
            )
            result = abjad.select.partition_by_counts(
                result, self.page_break_counts, cyclic=True, overhang=False
            )

            for item in result:
                abjad.attach(lit, item[-1])

    def _cache_persistent_info(self):
        print("Caching persistent info ...")
        info = dict()
        for i, voice in enumerate(
            abjad.select.components(
                self.score_template["Staff Group"], abjad.Staff
            )  # was Voice
        ):
            penultimate_rest = abjad.select.leaves(voice)[-2]
            persistent_attachments = abjad.get.indicators(penultimate_rest)
            info[f"Voice {i + 1}"] = persistent_attachments
        with open(f"{self.current_directory}/.persistent.py", "w") as fp:
            info_format_string = str(info)
            info_format_string = black.format_str(
                info_format_string, mode=black.mode.Mode()
            )
            string = f"import abjad\ninfo = {info_format_string}"
            fp.writelines(string)

    def _call_commands(self):
        if self.commands is None:
            return
        print("Calling commands ...")
        self.commands = flatten(self.commands)
        rhythm_commands_booleans = []
        for c in self.commands:
            if isinstance(c, RhythmCommand):
                rhythm_commands_booleans.append(True)
            else:
                rhythm_commands_booleans.append(False)
        if not any(rhythm_commands_booleans):
            self._fill_score_with_rests()
            self._add_ending_skips()
        for group_type, group in itertools.groupby(self.commands, lambda _: type(_)):
            if group_type == RhythmCommand:
                rhythm_group = [_ for _ in group]
                self._make_containers(rhythm_group)
            elif group_type == MusicCommand:
                music_command_group = [_ for _ in group]
                self._interpret_music_commands(music_command_group)
            elif group_type == HandlerCommand:
                handler_group = [_ for _ in group]
                self.call_handlers(handler_group)
            elif group_type == str:
                for s in group:
                    if s == "skips":
                        self._add_ending_skips()
            else:
                for command in group:
                    command(self.score_template)

    def call_handlers(self, commands):  # bypasses grace notes?
        print("Calling handlers ...")
        handler_to_value = dict()
        voice_names = sorted(set(_.voice_name for _ in commands))
        command_groups = []
        for handler_type, command_group in itertools.groupby(
            commands, lambda _: type(_.handler)
        ):
            group = [_ for _ in command_group]
            command_groups.append(group)
        for group in command_groups:
            voice_collections = dict()
            global_collection = consort.LogicalTieCollection()
            for tie in abjad.select.logical_ties(self.score_template["Global Context"]):
                global_collection.insert(tie)
            voice_collections["Global Context"] = global_collection
            for voice in abjad.select.components(self.score_template, abjad.Voice):
                collection = consort.LogicalTieCollection()
                for tie in abjad.select.logical_ties(voice):
                    collection.insert(tie)
                voice_collections[voice.name] = collection
            for v_name in voice_names:
                voice_command_list = [
                    command for command in group if command.voice_name == v_name
                ]
                voice_command_list.sort(key=lambda _: _.timespan)
                for command in voice_command_list:
                    voice_tie_collection = voice_collections[command.voice_name]
                    target_timespan = command.timespan
                    selection = [
                        _
                        for _ in voice_tie_collection.find_logical_ties_starting_during_timespan(
                            target_timespan
                        )
                    ]
                    if not selection:
                        continue
                    handler = command.handler
                    handler(selection)
                    handler_to_value[handler.name] = handler.state()
        with open(f"{self.current_directory}/.handlers.py", "w") as fp:
            handler_string = str(handler_to_value)
            string = black.format_str(handler_string, mode=black.mode.Mode())
            string = f"import abjad\nhandler_to_value = {string}"
            fp.writelines(string)

    @staticmethod
    def comment_measure_numbers(score):
        """
        Comments measure numbers in ``score``.
        """
        offset_to_measure_number = {}
        for context in abjad.iterate.components(score, abjad.Context):
            if not context.simultaneous:
                break
        site = abjad.Tag("evans.SegmentMaker.comment_measure_numbers()")
        leaves = abjad.select.leaves(context)
        measures = abjad.select.group_by_measure(leaves)
        for i, measure in enumerate(measures):
            measure_number = i + 1
            first_leaf = abjad.select.leaf(measure, 0)
            start_offset = first_leaf._get_timespan().start_offset
            offset_to_measure_number[start_offset] = measure_number
        for leaf in abjad.iterate.leaves(score):
            offset = leaf._get_timespan().start_offset
            measure_number = offset_to_measure_number.get(offset, None)
            if measure_number is None:
                continue
            context = abjad.Parentage(leaf).get(abjad.Context)
            if context.name is None:
                string = f"% [{context.lilypond_type} measure {measure_number}]"
            else:
                string = f"% [{context.name} measure {measure_number}]"
            literal = abjad.LilyPondLiteral(string, "absolute_before")
            tag = abjad.Tag("COMMENT_MEASURE_NUMBERS").append(site)
            abjad.attach(literal, leaf, tag=tag)

    def _extract_parts(self):
        print("Extracting parts ...")
        for count, staff in enumerate(
            abjad.iterate.components(self.score_template["Staff Group"], abjad.Staff)
        ):
            t = rf"\tag #'voice{count + 1}"
            literal = abjad.LilyPondLiteral(t, site="before")
            container = abjad.Container()
            abjad.attach(literal, container)
            abjad.mutate.wrap(staff, container)
        for count, group in enumerate(
            abjad.iterate.components(
                self.score_template["Staff Group"], abjad.StaffGroup
            )
        ):
            t = rf"\tag #'group{count + 1}"
            literal = abjad.LilyPondLiteral(t, site="before")
            container = abjad.Container()
            abjad.attach(literal, container)
            abjad.mutate.wrap(group, container)

    def _fill_score_with_rests(self):
        temp_leaf_maker = abjad.LeafMaker()
        for voice in abjad.select.components(self.score_template, abjad.Voice):
            durations = [
                abjad.Duration(time_signature)
                for time_signature in self.time_signatures[:-1]
            ]
            none_list = [None]
            full_voice_rests = temp_leaf_maker(none_list, durations)
            voice.extend(full_voice_rests)

        if self.fermata_measures is not None:
            for voice in abjad.select.components(self.score_template, abjad.Voice):
                measures = abjad.select.leaves(voice).group_by_measure()
                for fermata_index in self.fermata_measures:
                    make_fermata_measure(
                        measures[fermata_index], transparent=self.transparent_fermatas
                    )

        g_c = self.score_template["Global Context"]
        leaves = abjad.select.leaves(g_c)
        measures = abjad.select.group_by_measure(leaves)
        if self.fermata_measures is not None:
            for fermata_index in self.fermata_measures:
                make_fermata_measure(measures[fermata_index])
                self.time_signatures[fermata_index] = abjad.TimeSignature((1, 4))

        for voice in abjad.select.components(self.score_template, abjad.Voice):
            beautify_tuplets(voice)

    def _interpret_music_commands(self, music_commands):
        for music_command in music_commands:
            if music_command.threaded_commands is None:
                command_location = music_command.location
                command_voice_name = command_location[0]
                command_measures = command_location[1]
                duration_preprocessor = music_command.preprocessor

                global_context = self.score_template["Global Context"]
                global_leaves = abjad.select.leaves(global_context, abjad.Skip)
                signatures = [
                    abjad.get.indicator(_, abjad.TimeSignature) for _ in global_leaves
                ]
                non_reduced_fractions = [
                    abjad.NonreducedFraction(_) for _ in signatures
                ]

                relevant_voice = self.score_template[command_voice_name]
                if isinstance(command_measures, int):
                    relevant_measure_indices = [command_measures]
                elif isinstance(command_measures, tuple):
                    relevant_measure_indices = [
                        _ for _ in range(command_measures[0], command_measures[1])
                    ]
                else:
                    relevant_measure_indices = command_measures
                leaves = abjad.select.leaves(relevant_voice[:])
                measures = abjad.select.group_by_measure(leaves)
                relevant_measures = abjad.select.get(measures, relevant_measure_indices)
                measure_durations = [
                    non_reduced_fractions[_] for _ in relevant_measure_indices
                ]
                measure_groups = relevant_measures.group_by_contiguity()
                group_sizes = [len(g) for g in measure_groups]
                duration_groups = Sequence(measure_durations).partition_by_counts(
                    group_sizes
                )
                for measure_group, duration_group in zip(
                    measure_groups, duration_groups
                ):
                    measure_group = measure_group.flatten()
                    temp_container = abjad.Container()
                    if duration_preprocessor is not None:  # EXPERIMENTAL
                        duration_group = duration_preprocessor(duration_group)
                    new_leaves = music_command.callables[0].callable(duration_group)
                    if isinstance(new_leaves, list):
                        temp_container.extend(new_leaves)
                    else:
                        temp_container.append(new_leaves)
                    group_parents = [
                        abjad.get.parentage(_).parent for _ in measure_group
                    ]
                    group_parents_booleans = [
                        isinstance(_, abjad.Tuplet) for _ in group_parents
                    ]
                    beautify_tuplets(temp_container)
                    if not any(group_parents_booleans):
                        old_starting_leaf = measure_group[0]
                        old_starting_indicators = abjad.get.indicators(
                            old_starting_leaf
                        )
                        new_starting_leaf_target = abjad.select.leaf(temp_container, 0)
                        for old_indicator in old_starting_indicators:
                            abjad.attach(old_indicator, new_starting_leaf_target)
                        abjad.mutate.replace(measure_group, temp_container[:])
                    else:
                        top_level_components = get_top_level_components_from_leaves(
                            measure_group
                        )
                        old_starting_leaf = abjad.select.leaf(top_level_components, 0)
                        old_starting_indicators = abjad.get.indicators(
                            old_starting_leaf
                        )
                        new_starting_leaf_target = abjad.select.leaf(temp_container, 0)
                        for old_indicator in old_starting_indicators:
                            abjad.attach(old_indicator, new_starting_leaf_target)
                        abjad.mutate.replace(top_level_components, temp_container[:])

                if self.extra_rewrite is True:
                    SegmentMaker.rewrite_meter_without_splitting(
                        self.score_template
                    )  # EXPERIMENTAL

                for _callable in music_command.callables[1:]:
                    leaves = abjad.select.leaves(relevant_voice)
                    measures = abjad.select.group_by_measure(leaves)
                    relevant_measures = abjad.select.get(
                        measures, relevant_measure_indices
                    )
                    application_site = _callable.selector(relevant_measures)
                    _callable.callable(application_site)
                    if isinstance(_callable.callable, PitchHandler):
                        leaves = abjad.select.leaves(relevant_voice)
                        measures = abjad.select.group_by_measure(leaves)
                        relevant_measures = abjad.select.get(
                            measures, relevant_measure_indices
                        )
                        for leaf in abjad.select.leaves(
                            relevant_measures, pitched=True
                        ):
                            abjad.annotate(leaf, "pitched", True)

                for _attachment in music_command.attachments:
                    leaves = abjad.select.leaves(relevant_voice)
                    measures = abjad.select.group_by_measure(leaves)
                    relevant_measures = abjad.select.get(
                        measures, relevant_measure_indices
                    )
                    attachment_site = _attachment.selector(relevant_measures)
                    if isinstance(
                        attachment_site, list
                    ):  # WARNING: formerly tested against both list and selection
                        for site in attachment_site:
                            abjad.attach(_attachment.indicator, site)
                    else:
                        abjad.attach(_attachment.indicator, attachment_site)

            elif isinstance(music_command.threaded_commands, list):
                self._interpret_music_commands(music_command.threaded_commands)

    def _make_global_context(self):
        print("Making global context ...")

        for time_signature in self.time_signatures:
            skip = abjad.Skip(1, multiplier=(time_signature))
            abjad.attach(time_signature, skip, tag=abjad.Tag("scaling time signatures"))
            self.score_template["Global Context"].append(skip)

    def _make_containers(self, commands):
        print("Making containers ...")

        def make_container(handler, durations):
            selections = handler(durations)
            container = abjad.Container([])
            container.extend(selections)
            return container

        voice_names = sorted(set(_.voice_name for _ in commands))
        handler_to_value = dict()
        for voice_name in voice_names:
            voice_commands = [_ for _ in commands if _.voice_name == voice_name]
            voice_commands.sort(key=lambda _: _.timespan)
            for handler, grouper in itertools.groupby(
                voice_commands, key=lambda _: _.handler
            ):
                durations = [command.timespan.duration for command in grouper]
                container = make_container(handler, durations)
                voice = self.score_template[voice_name]
                voice.append(container[:])
                handler_to_value[handler.name] = handler.return_state()
        with open(f"{self.current_directory}/.rhythm.py", "w") as fp:
            handler_string = str(handler_to_value)
            string = black.format_str(handler_string, mode=black.mode.Mode())
            string = f"import abjad\nhandler_to_value = {string}"
            fp.writelines(string)

    def _make_mm_rests(self):
        print("Making MM rests ...")
        for voice in abjad.iterate.components(
            self.score_template["Staff Group"], abjad.Staff
        ):
            rhythm_commands_booleans = []
            for c in self.commands:
                if isinstance(c, RhythmCommand):
                    rhythm_commands_booleans.append(True)
                else:
                    rhythm_commands_booleans.append(False)
            if any(rhythm_commands_booleans):
                leaves = abjad.select.leaves(voice, grace=False)
                shards = abjad.mutate.split(leaves, self.time_signatures)
            else:
                leaves = abjad.select.components(voice)[2:]
                shards = abjad.select.group_by_measure(leaves)
            for i, shard in enumerate(shards[:-1]):
                if not all(isinstance(leaf, abjad.Rest) for leaf in shard):
                    continue
                indicators = abjad.get.indicators(shard[0])
                multiplier = abjad.get.duration(shard) / 2
                invisible_rest = abjad.Rest(1, multiplier=(multiplier))
                rest_literal = abjad.LilyPondLiteral(
                    r"\once \override Rest.transparent = ##t", "before"
                )
                abjad.attach(
                    rest_literal, invisible_rest, tag=abjad.Tag("applying invisibility")
                )
                for indicator in indicators:
                    abjad.attach(
                        indicator, invisible_rest, tag=abjad.Tag("applying indicators")
                    )
                multimeasure_rest = abjad.MultimeasureRest(1, multiplier=(multiplier))
                start_command = abjad.LilyPondLiteral(
                    r"\stopStaff \once \override Staff.StaffSymbol.line-count = #1 \startStaff",
                    site="before",
                )
                stop_command = abjad.LilyPondLiteral(
                    r"\stopStaff \startStaff", site="after"
                )
                if self.cutaway is True:
                    abjad.attach(
                        start_command, invisible_rest, tag=abjad.Tag("applying cutaway")
                    )
                    abjad.attach(
                        stop_command,
                        multimeasure_rest,
                        tag=abjad.Tag("applying cutaway"),
                    )
                    both_rests = [invisible_rest, multimeasure_rest]
                    abjad.mutate.replace(shard, both_rests[:])
                else:
                    both_rests = [invisible_rest, multimeasure_rest]
                    abjad.mutate.replace(shard, both_rests[:])

    def _remove_final_grand_pause(self):
        if self.add_final_grand_pause is True:
            return
        print("Removing final grand pause ...")
        for staff in abjad.select.components(
            self.score_template["Global Context"], abjad.Staff
        ):
            grand_pause = abjad.mutate.split(staff[:], self.time_signatures)[-1]
            for _ in grand_pause:
                staff.remove(_)
        for staff in abjad.select.components(
            self.score_template["Staff Group"],
            abjad.Staff,  # was voice double check for older scores
        ):
            main_voice = abjad.select.components(staff, abjad.Voice)[0]
            leaves = abjad.select.leaves(main_voice)
            grand_pause = abjad.select.group_by_measure(leaves)[-1]
            for _ in grand_pause:
                main_voice.remove(_)

    def _render_file(self):
        print("Rendering file ...")
        type(self).comment_measure_numbers(self.score_template)
        if self.with_layout is False:
            score_block = abjad.Block(name="score")
            score_block.items.append(self.score_template)
            assembled_includes = [f'\\include "{path}"' for path in self.score_includes]
            assembled_includes.append(score_block)
            score_file = abjad.LilyPondFile(
                items=assembled_includes,
            )
            for leaf in abjad.iterate.leaves(self.score_template):
                literal = abjad.LilyPondLiteral("", "absolute_before")
                abjad.attach(literal, leaf, tag=None)
            for container in abjad.iterate.components(
                self.score_template, abjad.Container
            ):
                if hasattr(container, "_main_leaf"):
                    literal = abjad.LilyPondLiteral("", "absolute_after")
                    abjad.attach(literal, container, tag=None)
                else:
                    literal = abjad.LilyPondLiteral("", "absolute_before")
                    abjad.attach(literal, container, tag=None)
                literal = abjad.LilyPondLiteral("", "closing")
                abjad.attach(literal, container, tag=None)
            directory = self.current_directory
            pdf_path = pathlib.Path(f"{directory}/illustration.pdf")
            ly_path = pathlib.Path(f"{directory}/illustration.ly")
            if pdf_path.exists():
                pdf_path.unlink()
            if ly_path.exists():
                ly_path.unlink()
            print("Persisting ...")  # was f"Persisting {baca.trim(pdf_path)} ..."
            abjad.persist.as_ly(
                score_file,
                ly_path,
                # align_tags=79,
            )
            if ly_path.exists():
                print("Rendering ...")  # was f"Opening {baca.trim(pdf_path)} ..."
                os.system(
                    f"run-lilypond {ly_path} >/dev/null 2>&1"
                )  # >/dev/null 2>&1 surpresses output
            if pdf_path.exists():
                print("Opening ...")  # was f"Opening {baca.trim(pdf_path)} ..."
                os.system(f"open {pdf_path}")
            with open(f"{directory}/illustration.ly") as pointer_1:
                score_lines = pointer_1.readlines()
                build_path = self.current_directory.parent.with_name("build")
                build_path /= "score"
                lines = score_lines[14:-1]  # was 15:-1
                with open(f"{build_path}/{self.segment_name}.ly", "w") as fp:
                    fp.writelines(lines)
        else:
            score_block = abjad.Block(name="score")
            parallel_container = abjad.Container(simultaneous=True)
            parallel_container.append(self.score_template)
            score_block.items.append(parallel_container)
            assembled_includes = [f'\\include "{path}"' for path in self.score_includes]
            assembled_includes.append(score_block)
            score_file = abjad.LilyPondFile(
                items=assembled_includes,
            )
            for leaf in abjad.iterate.leaves(self.score_template):
                literal = abjad.LilyPondLiteral("", "absolute_before")
                abjad.attach(literal, leaf, tag=None)
            for container in abjad.iterate.components(
                self.score_template, abjad.Container
            ):
                if hasattr(container, "_main_leaf"):
                    literal = abjad.LilyPondLiteral("", "absolute_after")
                    abjad.attach(literal, container, tag=None)
                else:
                    literal = abjad.LilyPondLiteral("", "absolute_before")
                    abjad.attach(literal, container, tag=None)
                literal = abjad.LilyPondLiteral("", "closing")
                abjad.attach(literal, container, tag=None)
            directory = self.current_directory
            pdf_path = pathlib.Path(f"{directory}/illustration.pdf")
            ly_path = pathlib.Path(f"{directory}/illustration.ly")
            if pdf_path.exists():
                pdf_path.unlink()
            if ly_path.exists():
                ly_path.unlink()
            print("Persisting ...")  # was f"Persisting {baca.trim(pdf_path)} ..."
            file_string = abjad.lilypond(score_file, tags=True)
            file_strings = file_string.splitlines(keepends=True)
            file_string_pre = file_strings[:14]
            file_string_mid = r"""      { \include "layout.ly" }"""
            file_string_post = file_strings[14:]
            with open(f"{directory}/illustration.ly", "w") as fp_pointer:
                final_string = file_string_pre
                final_string.extend(file_string_mid)
                final_string.extend(file_string_post)
                fp_pointer.writelines(final_string)
            layout_path = pathlib.Path(f"{directory}/layout.py")
            os.system(f"python {layout_path}")
            if ly_path.exists():
                print("Rendering ...")  # was f"Opening {baca.trim(pdf_path)} ..."
                os.system(
                    f"run-lilypond {ly_path} >/dev/null 2>&1"
                )  # >/dev/null 2>&1 surpresses output
            if pdf_path.exists():
                print("Opening ...")  # was f"Opening {baca.trim(pdf_path)} ..."
                os.system(f"open {pdf_path}")
            with open(f"{directory}/illustration.ly") as pointer_1:
                score_lines = pointer_1.readlines()
                build_path = self.current_directory.parent.with_name("build")
                build_path /= "score"
                lines = score_lines[12:14] + score_lines[15:-3]
                with open(f"{build_path}/{self.segment_name}.ly", "w") as fp:
                    fp.writelines(lines)

    def rewrite_meter(target):
        print("Rewriting meter ...")
        global_skips = [_ for _ in abjad.select.leaves(target["Global Context"])]
        sigs = []
        for skip in global_skips:
            for indicator in abjad.get.indicators(skip):
                if isinstance(indicator, abjad.TimeSignature):
                    sigs.append(indicator)
        for voice in abjad.select.components(target["Staff Group"], abjad.Voice):
            voice_dur = abjad.get.duration(voice)
            time_signatures = sigs[:-1]
            durations = [_.duration for _ in time_signatures]
            sig_dur = sum(durations)
            assert voice_dur == sig_dur, (voice_dur, sig_dur)
            shards = abjad.mutate.split(voice[:], durations)
            for i, shard in enumerate(shards):
                time_signature = sigs[i]
                inventories = [
                    x
                    for x in enumerate(
                        abjad.Meter(time_signature.pair).depthwise_offset_inventory
                    )
                ]
                if time_signature.denominator == 4:
                    abjad.Meter.rewrite_meter(
                        shard,
                        time_signature,
                        boundary_depth=inventories[-1][0],
                        rewrite_tuplets=False,
                    )
                else:
                    abjad.Meter.rewrite_meter(
                        shard,
                        time_signature,
                        boundary_depth=inventories[-2][0],
                        rewrite_tuplets=False,
                    )

    def rewrite_meter_without_splitting(target):
        global_skips = [_ for _ in abjad.select.leaves(target["Global Context"])]
        sigs = []
        for skip in global_skips:
            for indicator in abjad.get.indicators(skip):
                if isinstance(indicator, abjad.TimeSignature):
                    sigs.append(indicator)
        for voice in abjad.select.components(target["Staff Group"], abjad.Voice):
            voice_dur = abjad.get.duration(voice)
            time_signatures = sigs
            durations = [_.duration for _ in time_signatures]
            sig_dur = sum(durations)
            assert voice_dur == sig_dur, (voice_dur, sig_dur)
            leaves = abjad.select.leaves(voice[:])
            shards = abjad.select.group_by_measure(leaves)
            for i, shard in enumerate(shards):
                if not all(
                    isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest, abjad.Skip))
                    for leaf in abjad.select.leaves(shard)
                ):
                    time_signature = sigs[i]
                    top_level_components = get_top_level_components_from_leaves(shard)
                    shard = top_level_components
                    inventories = [
                        x
                        for x in enumerate(
                            abjad.Meter(time_signature.pair).depthwise_offset_inventory
                        )
                    ]
                    if time_signature.denominator == 4:
                        abjad.Meter.rewrite_meter(
                            shard,
                            time_signature,
                            boundary_depth=inventories[-1][0],
                            rewrite_tuplets=False,
                        )
                    elif time_signature.denominator == 16:  # experimental
                        abjad.Meter.rewrite_meter(
                            shard,
                            time_signature,
                            boundary_depth=inventories[0][0],
                            rewrite_tuplets=False,
                        )
                    else:
                        abjad.Meter.rewrite_meter(
                            shard,
                            time_signature,
                            boundary_depth=inventories[-2][0],
                            rewrite_tuplets=False,
                        )

    def transform_brackets(target):
        print("Transforming brackets ...")
        for tuplet in abjad.select.tuplets(target):
            if tuplet.multiplier.pair[1] % tuplet.multiplier.pair[0] > 1:
                if tuplet.diminution() is True:
                    tuplet.toggle_prolation()
            if tuplet.multiplier.pair[0] % tuplet.multiplier.pair[1] > 1:
                if tuplet.augmentation() is True:
                    tuplet.toggle_prolation()
            tuplet.normalize_multiplier()
            if tuplet.trivializable() is True:
                tuplet.trivialize()
            if tuplet.trivial() is True:
                tuplet.hide = True
            if abjad.get.sustained(tuplet) is True:
                inner_durs = []
                for _ in tuplet[:]:
                    if isinstance(_, abjad.Tuplet):
                        inner_durs.append(_.multiplied_duration)
                    else:
                        inner_durs.append(_.written_duration)
                tuplet_dur = sum(inner_durs)
                imp_num, imp_den = tuplet.implied_prolation.pair
                head_dur = tuplet_dur / imp_den
                dur = head_dur * imp_num
                maker = abjad.NoteMaker()
                donor_leaves = maker([0], [dur])
                indicators = abjad.get.indicators(tuplet[0])
                for indicator in indicators:
                    abjad.attach(indicator, donor_leaves[-1])
                abjad.mutate.replace(tuplet, donor_leaves[:])
            if tuplet.rest_filled() is True:
                inner_durs = []
                for _ in tuplet[:]:
                    if isinstance(_, abjad.Tuplet):
                        inner_durs.append(_.multiplied_duration)
                    else:
                        inner_durs.append(_.written_duration)
                tuplet_dur = sum(inner_durs)
                imp_num, imp_den = tuplet.implied_prolation.pair
                head_dur = tuplet_dur / imp_den
                dur = head_dur * imp_num
                maker = abjad.NoteMaker()
                abjad.mutate.replace(tuplet, maker([None], [dur]))
            if tuplet.hide is not True:
                notehead_maker = NoteheadBracketMaker()
                notehead_maker(tuplet)

    def _write_optimization_log(self):
        print("Writing optimization log ...\n")
        times = [self.pre_handlers_time + self.handlers_time + self.post_handlers_time]
        segment_time = sum(times)
        with open(f"{self.current_directory}/.optimization", "a") as fp:

            segment_time = f"Segment runtime: {segment_time} "
            segment_time += abjad.string.pluralize("second", segment_time)

            pre_handlers_time = f" Pre-handlers runtime: {self.pre_handlers_time} "
            pre_handlers_time += abjad.string.pluralize(
                "second", self.pre_handlers_time
            )

            handlers_time = f" Handlers runtime: {self.handlers_time} "
            handlers_time += abjad.string.pluralize("second", self.handlers_time)

            post_handlers_time = f" Post-handlers runtime: {self.post_handlers_time} "
            post_handlers_time += abjad.string.pluralize(
                "second", self.post_handlers_time
            )

            lines = []
            lines.append("")
            lines.append("")
            lines.append(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(segment_time)
            lines.append(pre_handlers_time)
            lines.append(handlers_time)
            lines.append(post_handlers_time)
            string = "\n".join(lines)
            fp.write(string)

    ## EXPERIMENTAL

    def _extract_voice_info(self, score):
        score_pitches = []
        score_durations = []
        for voice in abjad.select.components(score, abjad.Voice):
            pitches = []
            durations = []
            for tie in abjad.select.logical_ties(
                voice,
            ):
                dur = abjad.get.duration(tie)
                durations.append(str(dur))
                if isinstance(tie[0], abjad.Rest):
                    sub_pitches = ["Rest()"]
                else:
                    if abjad.get.annotation(tie[0], "ratio"):
                        sub_pitches = [abjad.get.annotation(tie[0], "ratio")]
                    else:
                        sub_pitches = [p.hertz for p in abjad.get.pitches(tie[0])]
                if 1 < len(sub_pitches):
                    pitches.append([str(s) for s in sub_pitches])
                elif 0 == len(sub_pitches):
                    pitches.append("Rest()")
                else:
                    pitches.append(str(sub_pitches[0]))
            score_pitches.append(pitches)
            score_durations.append(durations)
        return [_ for _ in zip(score_pitches, score_durations)]

    def _make_sc_file(self):
        info = self._extract_voice_info(self.score_template)
        lines = "s.boot;\ns.quit;\n\n("

        for i, voice in enumerate(info):
            lines += f"\n\t// voice {i + 1}\n\t\tPbind(\n\t\t\t\\freq, Pseq(\n"

            lines += "\t\t\t\t[\n"
            for chord in voice[0]:
                lines += "\t\t\t\t\t[\n"
                if isinstance(chord, list):
                    for _ in chord:
                        if _ == "Rest()":
                            lines += f"\t\t\t\t\t\t{_},\n"
                        else:
                            if _[0] == "[":
                                lines += f"\t\t\t\t\t\t{_[2:-2]},\n"
                            else:
                                lines += f"\t\t\t\t\t\t{_},\n"
                else:
                    if chord == "Rest()":
                        lines += f"\t\t\t\t\t\t{chord},\n"
                    else:
                        if chord[0] == "[":
                            lines += f"\t\t\t\t\t\t{chord[2:-2]},\n"
                        else:
                            lines += f"\t\t\t\t\t\t{chord},\n"
                lines += "\t\t\t\t\t],\n"
            lines += "\t\t\t\t],\n"
            lines += "\t\t\t),\n"
            lines += "\t\t\t\\dur, Pseq(\n\t\t\t\t[\n"
            for dur in voice[1]:
                lines += f"\t\t\t\t\t{quicktions.Fraction(dur) * 4} * {quicktions.Fraction(60, self.tempo[-1])},\n"
            lines += "\t\t\t\t]\n"
            lines += "\t\t\t,1),\n"
            lines += "\t\t\t\\legato, 1,\n\t\t).play;"

        lines += ")"

        with open(
            f'{self.current_directory}/voice_to_sc_{str(datetime.datetime.now()).replace(" ", "-").replace(":", "-").replace(".", "-")}.scd',
            "w",
        ) as fp:
            fp.writelines(lines)

    def build_segment(self):
        with abjad.Timer() as timer:
            self._make_global_context()
        self.pre_handlers_time = int(timer.elapsed_time)
        with abjad.Timer() as timer:
            self._call_commands()
        self.handlers_time = int(timer.elapsed_time)
        with abjad.Timer() as timer:
            if self.mm_rests:
                self._make_mm_rests()
            self._add_attachments()
            self._cache_persistent_info()
            self._remove_final_grand_pause()
            self._extract_parts()
            self._break_pages()
            self._render_file()
        self.post_handlers_time = int(timer.elapsed_time)
        self._write_optimization_log()


def beam_meter(components, meter, offset_depth, include_rests=True):
    r"""

    .. container:: example

        >>> pre_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
        >>> tuplet = abjad.Tuplet((2, 3), "c'8 r8 c'8")
        >>> post_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
        >>> staff = abjad.Staff()
        >>> combined = pre_tuplet_notes[:] + [tuplet] + post_tuplet_notes[:]
        >>> for _ in combined:
        ...     staff.append(_)
        ...
        >>> evans.beam_meter(components=staff[:], meter=abjad.Meter((4, 4)), offset_depth=1)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=["#(set-default-paper-size \"a4\" \'portrait)", r"#(set-global-staff-size 16)", "\\include \'abjad.ily\'", score],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \override Staff.Stem.stemlet-length = 0.75
                c'8
                [
                \revert Staff.Stem.stemlet-length
                c'8
                ]
                c'8
                \times 2/3 {
                    \override Staff.Stem.stemlet-length = 0.75
                    c'8
                    [
                    r8
                    \revert Staff.Stem.stemlet-length
                    c'8
                    ]
                }
                c'8
                \override Staff.Stem.stemlet-length = 0.75
                c'8
                [
                \revert Staff.Stem.stemlet-length
                c'8
                ]
            }

    """
    offsets = meter.depthwise_offset_inventory[offset_depth]
    offset_pairs = []
    for i, _ in enumerate(offsets[:-1]):
        offset_pair = [offsets[i], offsets[i + 1]]
        offset_pairs.append(offset_pair)
    initial_offset = abjad.get.timespan(components[0]).start_offset
    for i, pair in enumerate(offset_pairs):
        for i_, item in enumerate(pair):
            offset_pairs[i][i_] = item + initial_offset
    offset_timespans = [
        abjad.Timespan(start_offset=pair[0], stop_offset=pair[1])
        for pair in offset_pairs
    ]

    tup_list = [tup for tup in abjad.select.tuplets(components)]
    for t in tup_list:
        if isinstance(abjad.get.parentage(t).components[1], abjad.Tuplet) is False:
            # first_leaf = abjad.select.leaf(t, 0)
            # if not hasattr(first_leaf._overrides, "Beam"):
            abjad.beam(
                t[:],
                beam_rests=include_rests,
                stemlet_length=0.75,
                beam_lone_notes=False,
                selector=lambda _: abjad.select.leaves(_, grace=False),
            )
        else:
            continue

    non_tup_list = []
    for leaf in abjad.select.leaves(components):
        if isinstance(abjad.get.parentage(leaf).components[1], abjad.Tuplet) is False:
            non_tup_list.append(leaf)

    beamed_groups = []
    for i in enumerate(offset_timespans):
        beamed_groups.append([])

    for i, span in enumerate(offset_timespans):
        leaves = abjad.select.leaves(non_tup_list[:])
        for group in abjad.select.group_by(
            leaves,
            predicate=lambda x: abjad.get.timespan(x).happens_during_timespan(span),
        ):
            if abjad.get.timespan(group).happens_during_timespan(span) is True:
                beamed_groups[i].append(group[:])

    for subgroup in beamed_groups:
        subgrouper = abjad.select.group_by_contiguity(subgroup)
        for beam_group in subgrouper:
            # if not all(isinstance(leaf, abjad.Rest) for leaf in beam_group)
            abjad.beam(
                beam_group[:],
                beam_rests=include_rests,
                stemlet_length=0.75,
                beam_lone_notes=False,
                selector=lambda _: abjad.select.leaves(_, grace=False),
            )


def annotate_leaves(score, prototype=abjad.Leaf):
    for voice in abjad.select.components(score, abjad.Voice):
        if prototype is not None:
            abjad.label.with_indices(voice, prototype=prototype)
        else:
            abjad.label.with_indices(voice)


def annotate_time(context):
    abjad.label.with_start_offsets(context, clock_time=True)


def make_fermata_measure(selection, transparent=True):
    duration = abjad.Duration((1, 4))
    skip = abjad.MultimeasureRest(1, multiplier=duration)
    transparent_command = abjad.LilyPondLiteral(
        r"\once \override MultiMeasureRest.transparent = ##t",
        site="before",
    )
    temp_container = abjad.Container()
    temp_container.append(skip)
    original_leaves = selection.leaves()
    if abjad.get.has_indicator(original_leaves[0], abjad.TimeSignature):
        regular_rest = abjad.Rest(1, multiplier=duration / 2)
        first_skip = abjad.Skip(1, multiplier=duration / 2)
        temp_container = abjad.Container()
        temp_container.extend([first_skip, regular_rest])
        new_sig = abjad.TimeSignature((1, 4))
        abjad.attach(new_sig, temp_container[0])
        transparent_sig = abjad.LilyPondLiteral(
            r"\once \override Score.TimeSignature.transparent = ##t",
            site="before",
        )
        transparent_rest = abjad.LilyPondLiteral(
            r"\once \override Rest.transparent = ##t",
            site="before",
        )
        abjad.attach(transparent_sig, temp_container[0])
        abjad.attach(transparent_rest, temp_container[1])
    else:
        if transparent is True:
            start_command = abjad.LilyPondLiteral(
                r"\stopStaff \once \override Staff.StaffSymbol.line-count = #0 \startStaff",
                site="before",
            )
            stop_command = abjad.LilyPondLiteral(
                r"\stopStaff \startStaff", site="after"
            )
            abjad.attach(start_command, temp_container[0])
            abjad.attach(stop_command, temp_container[0])
    abjad.attach(transparent_command, temp_container[0])
    abjad.mutate.replace(original_leaves, temp_container[:])


def get_top_level_components_from_leaves(leaves):  # TODO:
    out = []
    for leaf in leaves:
        parent = abjad.get.parentage(leaf).parent
        if isinstance(parent, (abjad.Voice, abjad.Staff)):
            if leaf not in out:
                out.append(leaf)
        else:
            sub_out = get_top_level_components_from_leaves([parent])
            for sub_leaf in sub_out:
                if sub_leaf not in out:
                    out.append(sub_leaf)
    return out


def make_score_template(instruments, groups):
    assert sum(groups) == len(instruments)
    name_counts = {_.name: 1 for _ in instruments}
    sub_group_counter = 1
    score = abjad.Score(
        [
            abjad.Staff(name="Global Context", lilypond_type="TimeSignatureContext"),
            abjad.StaffGroup(name="Staff Group"),
        ],
        name="Score",
    )
    grouped_voices = Sequence(instruments).grouper(groups)
    for item in grouped_voices:
        if isinstance(item, list):
            sub_group = abjad.StaffGroup(
                name=f"sub group {sub_group_counter}", lilypond_type="PianoStaff"
            )
            sub_group_counter += 1
            for sub_item in item:
                if 1 < instruments.count(sub_item):
                    name_string = f"{sub_item.name} {name_counts[sub_item.name]}"
                else:
                    name_string = f"{sub_item.name}"
                staff = abjad.Staff(
                    [abjad.Voice(name=f"{name_string} voice")],
                    name=f"{name_string} staff",
                )
                sub_group.append(staff)
                name_counts[sub_item.name] += 1
            score["Staff Group"].append(sub_group)
        else:
            if 1 < instruments.count(item):
                name_string = f"{item.name} {name_counts[item.name]}"
            else:
                name_string = f"{item.name}"
            staff = abjad.Staff(
                [abjad.Voice(name=f"{name_string} voice")],
                name=f"{name_string} staff",
            )
            score["Staff Group"].append(staff)
            name_counts[item.name] += 1
    return score


def beautify_tuplets(target):
    for tuplet in abjad.select.tuplets(target):
        tuplet.denominator = 2
        if tuplet.multiplier.pair[1] % tuplet.multiplier.pair[0] > 1:
            if tuplet.diminution() is True:
                tuplet.toggle_prolation()
        if tuplet.multiplier.pair[0] % tuplet.multiplier.pair[1] > 1:
            if tuplet.augmentation() is True:
                tuplet.toggle_prolation()
        tuplet.normalize_multiplier()
        if tuplet.trivializable() is True:
            tuplet.trivialize()
        if tuplet.trivial() is True:
            tuplet.hide = True
        rests = abjad.select.rests(tuplet)
        for rest_group in abjad.select.group_by_contiguity(rests):
            abjad.mutate.fuse(rest_group)  # EXPERIMENTAL


def global_to_voice(score):
    global_context = score["Global Context"]
    leaves = abjad.select.leaves(global_context)
    measures = abjad.select.group_by_measure(leaves)
    voices = abjad.select.components(score, abjad.Voice)
    for i, measure in enumerate(measures):
        indicators = []
        for leaf in measure.leaves():
            for indicator in abjad.get.indicators(leaf):
                if not isinstance(
                    indicator, (abjad.TimeSignature, abjad.MetronomeMark)
                ):
                    indicators.append(indicator)
                    abjad.detach(indicator, leaf)
        for voice in voices:
            target = abjad.select.leaves(voice).group_by_measure().get([i]).leaf(0)
            for _indicator in indicators:
                abjad.attach(_indicator, target)


# experimental
def sort_voices(nested_input_list, voice_dict, prefill=True):
    def helper(values):
        already_used = []
        out = {}
        for value in values:
            out[values[0][1][0][0]] = values[0][0]
            already_used.append(values[0][1][0][0])
            values.remove(values[0])
            for value_ in values:
                for term in value_[1]:
                    if term[0] in already_used:
                        value_[1].remove(term)
            if 1 < len(values):
                values = sorted(values, key=lambda _: _[1][1])
            else:
                out[values[0][1][0][0]] = values[0][0]
        return out

    for i in range(len(voice_dict)):
        voice_dict[f"voice {i + 1}"].append(nested_input_list[0][i])

    for chord in nested_input_list[1:]:
        ratio_closeness_values = []
        for ratio in chord:
            temp_vals = [
                (voice, abs(voice_dict[voice][-1] - ratio)) for voice in voice_dict
            ]
            sorted_temp_vals = sorted(temp_vals, key=lambda _: _[1])
            ratio_closeness_values.append((ratio, sorted_temp_vals))
        sorted_ratio_closeness_values = sorted(
            ratio_closeness_values, key=lambda _: _[1][1]
        )
        distribution_dict = helper(sorted_ratio_closeness_values)
        for key in distribution_dict.keys():
            voice_dict[key].append(distribution_dict[key])

    return voice_dict


def _extract_voice_info(score):
    score_pitches = []
    score_durations = []
    for voice in abjad.select.components(score, abjad.Voice):
        pitches = []
        durations = []
        for tie in abjad.select.logical_ties(
            voice,
        ):
            dur = abjad.get.duration(tie)
            durations.append(str(dur))
            if isinstance(tie[0], abjad.Rest):
                sub_pitches = ["Rest()"]
            else:
                if abjad.get.annotation(tie[0], "ratio"):
                    sub_pitches = [abjad.get.annotation(tie[0], "ratio")]
                else:
                    sub_pitches = [p.hertz for p in abjad.get.pitches(tie[0])]
            if 1 < len(sub_pitches):
                pitches.append([str(s) for s in sub_pitches])
            elif 0 == len(sub_pitches):
                pitches.append("Rest()")
            else:
                pitches.append(str(sub_pitches[0]))
        score_pitches.append(pitches)
        score_durations.append(durations)
    return [_ for _ in zip(score_pitches, score_durations)]


# experimental
def make_sc_file(score, tempo, current_directory):

    info = _extract_voice_info(score)
    lines = "s.boot;\ns.quit;\n\n("

    for i, voice in enumerate(info):
        lines += f"\n\t// voice {i + 1}\n\t\tPbind(\n\t\t\t\\freq, Pseq(\n"

        lines += "\t\t\t\t[\n"
        for chord in voice[0]:
            lines += "\t\t\t\t\t[\n"
            if isinstance(chord, list):
                for _ in chord:
                    if _ == "Rest()":
                        lines += f"\t\t\t\t\t\t{_},\n"
                    else:
                        if _[0] == "[":
                            lines += f"\t\t\t\t\t\t{_[2:-2]},\n"
                        else:
                            lines += f"\t\t\t\t\t\t{_},\n"
            else:
                if chord == "Rest()":
                    lines += f"\t\t\t\t\t\t{chord},\n"
                else:
                    chord = chord.replace("'", "")
                    if chord[0] == "[":
                        lines += f"\t\t\t\t\t\t{chord[1:-1]},\n"
                    else:
                        lines += f"\t\t\t\t\t\t{chord},\n"
            lines += "\t\t\t\t\t],\n"
        lines += "\t\t\t\t],\n"
        lines += "\t\t\t),\n"
        lines += "\t\t\t\\dur, Pseq(\n\t\t\t\t[\n"
        for dur in voice[1]:
            lines += f"\t\t\t\t\t{quicktions.Fraction(dur) * 4} * {quicktions.Fraction(60, tempo.units_per_minute)},\n"
        lines += "\t\t\t\t]\n"
        lines += "\t\t\t,1),\n"
        lines += f"\t\t\t\\amp, {1 / len(info)},\n"
        lines += "\t\t\t\\legato, 1,\n\t\t).play;"

    lines += ")"

    with open(
        f'{current_directory}/voice_to_sc_{str(datetime.datetime.now()).replace(" ", "-").replace(":", "-").replace(".", "-")}.scd',
        "w",
    ) as fp:
        fp.writelines(lines)


def extract_class_name(instrument_class):
    instrument_string = str(instrument_class)

    out = ""

    for _ in instrument_string:

        if _ == "<":
            continue

        if _ == "(":
            break

        out += _

    word_list = abjad.string.delimit_words(out, separate_caps=True)

    new_out = " ".join(word_list)

    return new_out.lower()
