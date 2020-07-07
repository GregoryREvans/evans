import datetime
import itertools
import os
import time

import abjad
import evans


class SegmentMaker:
    def __init__(
        self,
        instruments=None,
        names=None,
        abbreviations=None,
        name_staves=True,
        rhythm_timespans=None,
        handler_timespans=None,
        score_template=None,
        time_signatures=None,
        clef_handlers=None,
        commands=None,
        tuplet_bracket_noteheads=True,
        add_final_grand_pause=True,
        fermata="scripts.ushortfermata",
        score_includes=None,
        segment_name=None,
        current_directory=None,
        build_path=None,
        cutaway=True,
        beam_pattern="runs",
        beam_rests=True,
        tempo=((1, 4), 90),
        rehearsal_mark=None,
        colophon=None,
        page_break_counts=None,
        barline="||",
    ):
        self.instruments = instruments
        self.names = names
        self.abbreviations = abbreviations
        self.name_staves = name_staves
        self.rhythm_timespans = rhythm_timespans
        self.handler_timespans = handler_timespans
        self.score_template = score_template
        self.time_signatures = time_signatures
        self.clef_handlers = clef_handlers
        self.commands = commands
        self.tuplet_bracket_noteheads = tuplet_bracket_noteheads
        self.add_final_grand_pause = add_final_grand_pause
        self.fermata = fermata
        self.score_includes = score_includes
        self.segment_name = segment_name
        self.current_directory = current_directory
        self.build_path = build_path
        self.cutaway = cutaway
        self.beam_pattern = beam_pattern
        self.beam_rests = beam_rests
        self.tempo = tempo
        self.rehearsal_mark = rehearsal_mark
        self.colophon = colophon
        self.page_break_counts = page_break_counts
        self.barline = barline
        self.time_1 = None
        self.time_2 = None
        self.time_3 = None
        self.time_4 = None
        self.time_5 = None
        self.time_6 = None

    def build_segment(self):
        self._interpret_file()
        self._making_containers()
        self._transform_brackets()
        self._splitting_and_rewriting()
        self._adding_ending_skips()
        self._apply_handlers()
        self._multimeasure_rests_and_cutaway()
        self._beaming_runs()
        self._adding_attachments()
        if self.commands is not None:
            self._commands()
        # self._transposing_and_adding_clefs()
        self._cache_persistent_info()
        if self.add_final_grand_pause is False:
            self._remove_final_grand_pause()
        self._extracting_parts()
        self._break_pages()
        self._render_file()
        self._write_optimization_log()

    def _interpret_file(self):

        self.time_1 = time.time()

        print("Interpreting file ...")

        global_timespan = abjad.Timespan(
            start_offset=0,
            stop_offset=max(_.stop_offset for _ in self.rhythm_timespans.values()),
        )

        for voice_name, timespan_list in self.rhythm_timespans.items():
            silences = abjad.TimespanList([global_timespan])
            silences.extend(timespan_list)
            silences.sort()
            silences.compute_logical_xor()
            for silence_timespan in silences:
                timespan_list.append(
                    abjad.AnnotatedTimespan(
                        start_offset=silence_timespan.start_offset,
                        stop_offset=silence_timespan.stop_offset,
                        annotation=evans.TimespanSpecifier(
                            handler=None, voice_name=voice_name
                        ),
                    )
                )
            timespan_list.sort()

        for time_signature in self.time_signatures:
            skip = abjad.Skip(1, multiplier=(time_signature))
            abjad.attach(time_signature, skip, tag=abjad.Tag("scaling time signatures"))
            self.score_template["Global Context"].append(skip)

    def _making_containers(self):

        print("Making containers ...")

        def key_function(timespan):
            return timespan.annotation.handler  # or silence_maker

        def make_container(handler, durations):
            selections = handler(durations)
            container = abjad.Container([])
            container.extend(selections)
            return container

        for voice_name, timespan_list in self.rhythm_timespans.items():
            handler_to_value = abjad.OrderedDict()
            for handler, grouper in itertools.groupby(timespan_list, key=key_function):
                durations = [timespan.duration for timespan in grouper]
                container = make_container(handler, durations)
                voice = self.score_template[voice_name]
                voice.append(container[:])
                handler_to_value[handler.name] = handler.return_state()
            with open(f"{self.current_directory}/.rhythm.py", "w") as fp:
                handler_to_value_format = format(handler_to_value)
                string = f"import abjad\nfrom abjad import *\nhandler_to_value = {handler_to_value_format}"
                fp.writelines(string)

    def _splitting_and_rewriting(self):

        print("Splitting and rewriting ...")
        for voice in abjad.iterate(self.score_template["Staff Group"]).components(
            abjad.Voice
        ):
            for i, shard in enumerate(
                abjad.mutate(voice[:]).split(self.time_signatures)
            ):
                time_signature = self.time_signatures[i]
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

    def _apply_handlers(self):
        print("Handlers ...")
        handler_to_value = abjad.OrderedDict()
        for t_list in self.handler_timespans:
            for voice_name, sub_timespan_list in t_list.items():
                voice_tie_selection = abjad.select(
                    self.score_template[voice_name]
                ).logical_ties()
                voice_tie_collection = evans.LogicalTieCollection()
                for tie in voice_tie_selection:
                    voice_tie_collection.insert(tie)
                for target_timespan in sub_timespan_list:
                    selection = abjad.Selection(
                        [
                            _
                            for _ in voice_tie_collection.find_logical_ties_starting_during_timespan(
                                target_timespan
                            )
                        ]
                    )
                    if not selection:
                        continue
                    handler = target_timespan.annotation.handler
                    handler(selection)
                    handler_to_value[handler.name] = handler.state()
        with open(f"{self.current_directory}/.handlers.py", "w") as fp:
            handler_to_value_format = format(handler_to_value)
            string = f"import abjad\nhandler_to_value = {handler_to_value_format}"
            fp.writelines(string)

    def _multimeasure_rests_and_cutaway(self):

        print("MM Rests and cutaway ...")

        for voice in abjad.iterate(self.score_template["Staff Group"]).components(
            abjad.Voice
        ):
            leaves = abjad.select(voice).leaves(grace=False)
            shards = abjad.mutate(leaves).split(self.time_signatures)
            for shard in shards[:-1]:
                if not all(isinstance(leaf, abjad.Rest) for leaf in shard):
                    continue
                indicators = abjad.inspect(shard[0]).indicators()
                multiplier = abjad.inspect(shard).duration() / 2
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
                    format_slot="before",
                )
                stop_command = abjad.LilyPondLiteral(
                    r"\stopStaff \startStaff", format_slot="after"
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
                    abjad.mutate(shard).replace(both_rests[:])
                else:
                    both_rests = [invisible_rest, multimeasure_rest]
                    abjad.mutate(shard).replace(both_rests[:])

    def _adding_ending_skips(self):

        print("Ending skips ...")

        last_skip = abjad.select(self.score_template["Global Context"]).leaves()[-1]
        override_command = abjad.LilyPondLiteral(
            r"\once \override TimeSignature.color = #white", format_slot="before"
        )
        abjad.attach(
            override_command, last_skip, tag=abjad.Tag("applying ending skips")
        )

        for voice in abjad.select(self.score_template["Staff Group"]).components(
            abjad.Voice
        ):
            container = abjad.Container()
            sig = self.time_signatures[-1]
            leaf_duration = sig.duration / 2
            rest_leaf = abjad.Rest(1, multiplier=(leaf_duration))
            mult_rest_leaf = abjad.MultimeasureRest(1, multiplier=(leaf_duration))
            container.append(rest_leaf)
            container.append(mult_rest_leaf)
            markup = abjad.Markup.musicglyph(self.fermata, direction=abjad.Up)
            markup.center_align()
            start_command = abjad.LilyPondLiteral(
                r"\stopStaff \once \override Staff.StaffSymbol.line-count = #0 \startStaff",
                format_slot="before",
            )
            stop_command = abjad.LilyPondLiteral(
                r"\stopStaff \startStaff", format_slot="after"
            )
            rest_literal = abjad.LilyPondLiteral(
                r"\once \override Rest.color = #white", "before"
            )
            mult_rest_literal = abjad.LilyPondLiteral(
                r"\once \override MultiMeasureRest.color = #white", "before"
            )
            penultimate_rest = container[0]
            final_rest = container[-1]
            abjad.attach(markup, final_rest, tag=abjad.Tag("applying ending skips"))
            abjad.attach(
                start_command, penultimate_rest, tag=abjad.Tag("applying ending skips")
            )
            if self.barline == "|.":
                stop_command = abjad.LilyPondLiteral(r"\stopStaff", format_slot="after")
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
            voice.append(container[:])

    def _transform_brackets(self):
        print("Transforming brackets ...")
        for tuplet in abjad.select(self.score_template).components(abjad.Tuplet):
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
            if tuplet.sustained() is True:
                dur = abjad.inspect(tuplet).duration()
                maker = abjad.NoteMaker()
                donor_leaves = maker([0], [dur])
                indicators = abjad.inspect(tuplet[0]).indicators()
                for indicator in indicators:
                    abjad.attach(indicator, donor_leaves[-1])
                abjad.mutate(tuplet).replace(donor_leaves[:])
            if tuplet.rest_filled() is True:
                dur = abjad.inspect(tuplet).duration()
                maker = abjad.NoteMaker()
                abjad.mutate(tuplet).replace(maker([None], [dur]))
            if tuplet.hide is not True:
                time_duration = tuplet.multiplied_duration
                imp_num, imp_den = tuplet.implied_prolation.pair
                notehead_wrapper = time_duration / imp_num
                wrapper_pair = notehead_wrapper.pair
                if wrapper_pair[0] == 3:
                    notehead_wrapper = wrapper_pair[1] // 2
                    dots = "."
                else:
                    notehead_wrapper = wrapper_pair[1]
                    dots = ""
                multiplier = 1
                if self.tuplet_bracket_noteheads is True:
                    abjad.tweak(
                        tuplet
                    ).TupletNumber.text = f'#(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text {imp_den * multiplier} {imp_num * multiplier}) "{notehead_wrapper}{dots}")'

    def _commands(self):
        print("Commands ...")
        for command in self.commands:
            command(self.score_template)

    def _beaming_runs(self):
        if self.beam_pattern == "runs":
            print("Beaming ...")
            for voice in abjad.select(self.score_template).components(abjad.Voice):
                for shard in abjad.mutate(voice[:]).split(self.time_signatures):
                    abjad.beam(shard[:], beam_lone_notes=False, beam_rests=False)
        elif self.beam_pattern == "meter":
            for voice in abjad.iterate(self.score_template["Staff Group"]).components(
                abjad.Voice
            ):
                for i, shard in enumerate(
                    abjad.mutate(voice[:]).split(self.time_signatures)
                ):
                    met = abjad.Meter(self.time_signatures[i].pair)
                    inventories = [
                        x
                        for x in enumerate(
                            abjad.Meter(
                                self.time_signatures[i].pair
                            ).depthwise_offset_inventory
                        )
                    ]
                    if self.time_signatures[i].denominator == 4:
                        evans.beam_meter(
                            components=shard[:],
                            meter=met,
                            offset_depth=inventories[-1][0],
                            include_rests=self.beam_rests,
                        )
                    else:
                        evans.beam_meter(
                            components=shard[:],
                            meter=met,
                            offset_depth=inventories[-2][0],
                            include_rests=self.beam_rests,
                        )
        else:
            pass
        for trem in abjad.select(self.score_template).components(
            abjad.TremoloContainer
        ):
            if abjad.StartBeam() in abjad.inspect(trem[0]).indicators():
                abjad.detach(abjad.StartBeam(), trem[0])
            if abjad.StopBeam() in abjad.inspect(trem[-1]).indicators():
                abjad.detach(abjad.StopBeam(), trem[-1])

    def _adding_attachments(self):

        print("Attachments ...")
        last_voice = abjad.select(self.score_template).components(abjad.Voice)[-1]
        colophon_leaf = abjad.select(last_voice).leaves()[-2]
        if self.colophon is not None:
            abjad.attach(self.colophon, colophon_leaf)

        if self.abbreviations is not None:
            abbreviations = []
            abb = self.abbreviations
            mark_abbreviations = [abjad.Markup(_) for _ in abb]
            for x in mark_abbreviations:
                x.hcenter_in(12)
                abbreviations.append(abjad.MarginMarkup(markup=x))
        else:
            abbreviations = [_ for _ in range(len(self.instruments))]
        if self.names is not None:
            names = []
            nm = self.names
            mark_names = [abjad.Markup(_) for _ in nm]
            for x in mark_names:
                x.hcenter_in(14)
                names.append(abjad.StartMarkup(markup=x))
        else:
            names = [_ for _ in range(len(self.instruments))]

        metro = abjad.MetronomeMark(self.tempo[0], self.tempo[1])
        # metro = abjad.MetronomeMark(custom_markup=metro.make_tempo_equation_markup())#remove if broken
        if self.tempo is not None:
            for staff in abjad.iterate(
                self.score_template["Global Context"]
            ).components(abjad.Staff):
                leaf1 = abjad.select(staff).leaves()[0]
                abjad.attach(metro, leaf1)

        markup2 = abjad.RehearsalMark(
            markup=abjad.Markup(fr"\bold {{ {self.rehearsal_mark} }}")
        )
        if self.rehearsal_mark is not None:
            for staff in abjad.iterate(
                self.score_template["Global Context"]
            ).components(abjad.Staff):
                leaf1 = abjad.select(staff).leaves()[0]
                abjad.attach(markup2, leaf1)

        bar_line = abjad.BarLine(self.barline)
        if self.barline is not None:
            for voice in abjad.iterate(self.score_template["Staff Group"]).components(
                abjad.Voice
            ):
                if self.barline == "|.":
                    last_leaf = abjad.select(voice).leaves()[-1]
                    abjad.attach(bar_line, last_leaf)
                else:
                    last_leaf = abjad.select(voice).leaves()[-3]
                    abjad.attach(bar_line, last_leaf)

        for abbrev, name, inst, handler, voice in zip(
            abbreviations,
            names,
            self.instruments,
            self.clef_handlers,
            abjad.select(self.score_template["Staff Group"]).components(abjad.Voice),
        ):
            first_leaf = abjad.select(voice).leaves()[0]
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
            abjad.Instrument.transpose_from_sounding_pitch(voice)
            handler(voice)

    def _remove_final_grand_pause(self):
        for staff in abjad.select(self.score_template["Global Context"]).components(
            abjad.Staff
        ):
            grand_pause = abjad.mutate(staff[:]).split(self.time_signatures)[-1]
            for _ in grand_pause:
                staff.remove(_)
        for voice in abjad.select(self.score_template["Staff Group"]).components(
            abjad.Voice
        ):
            grand_pause = abjad.mutate(voice[:]).split(self.time_signatures)[-1]
            for _ in grand_pause:
                voice.remove(_)

    def _cache_persistent_info(self):
        print("Caching persistent info ...")
        info = abjad.OrderedDict()
        for i, voice in enumerate(
            abjad.select(self.score_template["Staff Group"]).components(abjad.Voice)
        ):
            penultimate_rest = abjad.select(voice).leaves()[-2]
            persistent_attachments = abjad.inspect(penultimate_rest).indicators()
            info[f"Voice {i + 1}"] = persistent_attachments
        with open(f"{self.current_directory}/.persistent.py", "w") as fp:
            info_format = format(info)
            string = f"import abjad\ninfo = {info_format}"
            fp.writelines(string)

    def _break_pages(self):
        print("Breaking pages ...")
        if self.page_break_counts is not None:
            lit = abjad.LilyPondLiteral(r"\pageBreak", format_slot="absolute_after")
            result = abjad.select(self.score_template["Global Context"]).components(
                abjad.Skip
            )
            result = result.partition_by_counts(
                self.page_break_counts, cyclic=True, overhang=False
            )

            for item in result:
                abjad.attach(lit, item[-1])

    def _render_file(self):
        print("Rendering file ...")
        abjad.SegmentMaker.comment_measure_numbers(self.score_template)
        score_file = abjad.LilyPondFile.new(
            self.score_template, includes=self.score_includes
        )
        for leaf in abjad.iterate(self.score_template).leaves():
            literal = abjad.LilyPondLiteral("", "absolute_before")
            abjad.attach(literal, leaf, tag=None)
        for container in abjad.iterate(self.score_template).components(abjad.Container):
            if hasattr(container, "_main_leaf"):
                literal = abjad.LilyPondLiteral("", "absolute_after")
                abjad.attach(literal, container, tag=None)
            else:
                literal = abjad.LilyPondLiteral("", "absolute_before")
                abjad.attach(literal, container, tag=None)
            literal = abjad.LilyPondLiteral("", "closing")
            abjad.attach(literal, container, tag=None)
        self.time_2 = time.time()
        # ###################
        directory = self.current_directory
        pdf_path = abjad.Path(f"{directory}/illustration.pdf")
        if pdf_path.exists():
            pdf_path.unlink()
        self.time_3 = time.time()
        print(f"Persisting {pdf_path.trim()} ...")
        result = abjad.persist(score_file).as_pdf(pdf_path, strict=79)
        # print(result[0])
        # print(result[1])
        # print(result[2])
        success = result[3]
        if success is False:
            print("LilyPond failed!")
        self.time_4 = time.time()
        abjad_time = round(self.time_4 - self.time_3)
        print(f"Total persist time: {abjad_time} seconds")
        if pdf_path.exists():
            print(f"Opening {pdf_path.trim()} ...")
            os.system(f"open {pdf_path}")
        score_lines = open(f"{directory}/illustration.ly").readlines()
        build_path = (self.build_path / "score").resolve()
        open(f"{build_path}/{self.segment_name}.ly", "w").writelines(score_lines[15:-1])

        self.time_5 = time.time()

    def _extracting_parts(self):
        print("Extracting parts ...")
        for count, voice in enumerate(
            abjad.iterate(self.score_template["Staff Group"]).components(abjad.Voice)
        ):
            t = r"\tag #'" + f"voice{count + 1}" + r" {"
            pre_lit = abjad.LilyPondLiteral(t, format_slot="absolute_before")
            post_lit = abjad.LilyPondLiteral(r"}", format_slot="absolute_after")
            abjad.attach(pre_lit, voice)
            abjad.attach(post_lit, voice)
        self.time_6 = time.time()

    def _write_optimization_log(self):
        print("Writing optimization log ...")
        abjad_time = self.time_4 - self.time_3
        segment_time = self.time_2 - self.time_1
        parts_time = self.time_6 - self.time_5
        open(f"{self.current_directory}/.optimization", "a").writelines(
            f"{datetime.datetime.now()}\nSegment runtime: {int(round(segment_time))} seconds \nAbjad/Lilypond runtime: {int(round(abjad_time))} seconds \nParts extraction runtime: {int(round(parts_time))} seconds \n\n"
        )


# ###DEMO###
# from passagenwerk.Materials.score_structure.instruments import instruments as insts
# from passagenwerk.Materials.timespans.Segment_I.convert_timespans import (
#     segment_I_rhythm_timespans,
#     segment_I_timespans,
# )
# from passagenwerk.Materials.score_structure.score_structure import score
# from passagenwerk.Materials.score_structure.Segment_I.time_signatures import (
#     time_signatures,
# )
# from passagenwerk.Materials.score_structure.Segment_I.time_signatures import bounds
# from passagenwerk.Materials.rhythm.Segment_I.rhythm_handlers import * #does this need to be here?
# from passagenwerk.Materials.pitch.Segment_I.clef_handlers import clef_handlers
# from evans.abjad_functions.talea_timespan.timespan_functions import (
#     evans.TimespanSpecifier,
# )  # rename module
#
# maker = SegmentMaker(
#         instruments=insts,
#         rhythm_timespans=segment_I_rhythm_timespans,
#         handler_timespans=segment_I_timespans,
#         score_template=score,
#         time_signatures=time_signatures,
#         clef_handlers=clef_handlers,
#         score_includes=[
#             "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily",
#             "/Users/evansdsg2/Scores/passagenwerk/passagenwerk/Build/first_stylesheet.ily",
#         ],
#         parts_includes=[
#             "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily",
#             "/Users/evansdsg2/Scores/passagenwerk/passagenwerk/Build/parts_stylesheet.ily",
#         ],
#         segment_name="Segment_I"
#         # build_path=f"""{pathlib.Path(__file__).parent}""",
# )
#
# maker.build_segment()
