import abjad
import abjadext.rmakers
import evans
import itertools
import os
import pathlib
import time
import datetime


class SegmentMaker:
    def __init__(
        self,
        instruments=None,
        names=None,
        abbreviations=None,
        rhythm_timespans=None,
        handler_timespans=None,
        score_template=None,
        time_signatures=None,
        clef_handlers=None,
        score_includes=None,
        parts_includes=None,
        segment_name=None,
        current_directory=None,
        build_path=None,
        cutaway=True,
        beam_pattern="runs",
        #instrument names
        # instrument abbrev.
    ):
        self.instruments = instruments
        self.names = names
        self.abbreviations = abbreviations
        self.rhythm_timespans = rhythm_timespans
        self.handler_timespans = handler_timespans
        self.score_template = score_template
        self.time_signatures = time_signatures
        self.clef_handlers = clef_handlers
        self.score_includes = score_includes
        self.parts_includes = parts_includes
        self.segment_name = segment_name
        self.current_directory = current_directory
        self.build_path = build_path
        self.cutaway = cutaway
        self.beam_pattern = beam_pattern
        self.time_1 = None
        self.time_2 = None
        self.time_3 = None
        self.time_4 = None
        self.time_5 = None
        self.time_6 = None

    def build_segment(self):
        self._interpret_file()
        self._making_containers()
        self._splitting_and_rewriting()
        self._handlers()
        self._multimeasure_rests_and_cutaway()
        self._adding_ending_skips()
        self._beaming_runs()
        self._adding_attachments()
        # self._transposing_and_adding_clefs()
        self._render_file()
        self._extracting_parts()
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
                        annotation=TimespanSpecifier(
                            handler=None, voice_name=voice_name
                        ),
                    )
                )
            timespan_list.sort()

        for time_signature in self.time_signatures:
            skip = abjad.Skip(1, multiplier=(time_signature))
            abjad.attach(time_signature, skip, tag="scaling time signatures")
            self.score_template["Global Context"].append(skip)

    def _making_containers(self):

        print("Making containers ...")

        def key_function(timespan):
            return timespan.annotation.handler or silence_maker

        def make_container(handler, durations):
            selections = handler(durations)
            container = abjad.Container([])
            container.extend(selections)
            return container

        for voice_name, timespan_list in self.rhythm_timespans.items():
            for handler, grouper in itertools.groupby(timespan_list, key=key_function):
                durations = [timespan.duration for timespan in grouper]
                container = make_container(handler, durations)
                voice = self.score_template[voice_name]
                voice.append(container[:])

    def _splitting_and_rewriting(self):

        print("Splitting and rewriting ...")
        for voice in abjad.iterate(self.score_template["Staff Group"]).components(
            abjad.Voice
        ):
            for i, shard in enumerate(
                abjad.mutate(voice[:]).split(self.time_signatures)
            ):
                time_signature = self.time_signatures[i]
                abjad.mutate(shard).rewrite_meter(time_signature)  # , boundary_depth=1)

    def _handlers(self):

        print("Handlers ...")
        for list in self.handler_timespans:
            for voice_name, sub_timespan_list in list.items():
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
                    if len(selection) < 1:
                        continue
                    else:
                        target_timespan.annotation.handler(selection)

    def _multimeasure_rests_and_cutaway(self):

        print("Adding Multimeasure Rests and cutaway...")

        for voice in abjad.iterate(self.score_template["Staff Group"]).components(
            abjad.Voice
        ):
            leaves = abjad.select(voice).leaves()
            for shard in abjad.mutate(leaves).split(self.time_signatures):
                if not all(isinstance(leaf, abjad.Rest) for leaf in shard):
                    continue
                indicators = abjad.inspect(shard[0]).indicators()
                multiplier = abjad.inspect(shard).duration() / 2
                invisible_rest = abjad.Rest(1, multiplier=(multiplier))
                rest_literal = abjad.LilyPondLiteral(
                    r"\once \override Rest.transparent = ##t", "before"
                )
                abjad.attach(rest_literal, invisible_rest, tag="applying invisibility")
                for indicator in indicators:
                    abjad.attach(indicator, invisible_rest, tag="applying indicators")
                multimeasure_rest = abjad.MultimeasureRest(1, multiplier=(multiplier))
                start_command = abjad.LilyPondLiteral(
                    r"\stopStaff \once \override Staff.StaffSymbol.line-count = #1 \startStaff",
                    format_slot="before",
                )
                stop_command = abjad.LilyPondLiteral(
                    r"\stopStaff \startStaff", format_slot="after"
                )
                if self.cutaway is True:
                    abjad.attach(start_command, invisible_rest, tag="applying cutaway")
                    abjad.attach(stop_command, multimeasure_rest, tag="applying cutaway")
                    both_rests = [invisible_rest, multimeasure_rest]
                    abjad.mutate(shard).replace(both_rests[:])
                else:
                    both_rests = [invisible_rest, multimeasure_rest]
                    abjad.mutate(shard).replace(both_rests[:])

    def _adding_ending_skips(self):

        print("Adding ending skips ...")

        last_skip = abjad.select(self.score_template["Global Context"]).leaves()[-1]
        override_command = abjad.LilyPondLiteral(
            r"\once \override TimeSignature.color = #white", format_slot="before"
        )
        abjad.attach(override_command, last_skip, tag="applying ending skips")

        for voice in abjad.select(self.score_template["Staff Group"]).components(
            abjad.Voice
        ):
            last_run = abjad.select(voice).runs()[-1]
            container = abjad.Container()
            sig = self.time_signatures[-1]
            leaf_duration = sig.duration / 2
            rest_leaf = abjad.Rest(1, multiplier=(leaf_duration))
            mult_rest_leaf = abjad.MultimeasureRest(1, multiplier=(leaf_duration))
            container.append(rest_leaf)
            container.append(mult_rest_leaf)
            markup = abjad.Markup.musicglyph(
                "scripts.ushortfermata", direction=abjad.Up
            )
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
            abjad.attach(markup, final_rest, tag="applying ending skips")
            abjad.attach(start_command, penultimate_rest, tag="applying ending skips")
            abjad.attach(stop_command, final_rest, tag="applying ending skips")
            abjad.attach(rest_literal, penultimate_rest, tag="applying ending skips")
            abjad.attach(mult_rest_literal, final_rest, tag="applying ending skips")
            if abjad.inspect(last_run[0]).has_indicator(abjad.Dynamic):
                abjad.attach(
                    abjad.StopHairpin(), penultimate_rest, tag="applying ending skips"
                )
            else:
                continue
            voice.append(container[:])

    def _beaming_runs(self):
        if self.beam_pattern == "runs":
            print("Beaming runs ...")
            for voice in abjad.select(self.score_template).components(abjad.Voice):
                for run in abjad.select(voice).runs():
                    specifier = abjadext.rmakers.BeamSpecifier(beam_each_division=False)
                    specifier(run)
                abjad.beam(
                    voice[:],
                    beam_lone_notes=False,
                    beam_rests=False,
                )
        elif self.beam_pattern == "quarters":
            for voice in abjad.iterate(self.score_template["Staff Group"]).components(
                abjad.Voice
            ):
                for i, shard in enumerate(
                    abjad.mutate(voice[:]).split(self.time_signatures)
                ):
                    selector = abjad.select().leaves().partition_by_durations(
                        [abjad.Duration(1, 4)],
                        cyclic=True,
                        # fill=abjad.Exact,
                        fill=abjad.More,
                        # fill=abjad.Less,
                        in_seconds=False,
                        overhang=True,
                    )
                    result = selector(shard) # also split leaves by quarters to help beaming be exact?
                    for quarter in result:
                        abjad.beam(
                            quarter[:],
                            beam_lone_notes=False,
                            beam_rests=False,
                            # stemlet_length=2,
                        )
        else:
            pass

        # print('Stopping Hairpins and Text Spans...')
        # for staff in abjad.iterate(self.score_template['Staff Group']).components(abjad.Staff):
        #     for rest in abjad.iterate(staff).components(abjad.Rest):
        #         previous_leaf = abjad.inspect(rest).leaf(-1)
        #         if isinstance(previous_leaf, abjad.Note):
        #             abjad.attach(abjad.StopHairpin(), rest)
        #             abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpanOne'), rest)
        #             abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpanTwo'), rest)
        #             abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpanThree'), rest)
        #         elif isinstance(previous_leaf, abjad.Chord):
        #             abjad.attach(abjad.StopHairpin(), rest)
        #             abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpanOne'), rest)
        #             abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpanTwo'), rest)
        #             abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpanThree'), rest)
        #         elif isinstance(previous_leaf, abjad.Rest):
        #             pass
        # for staff in abjad.iterate(self.score_template['Staff Group']).components(abjad.Staff):
        #     for run in abjad.select(staff).runs():
        #         last_leaf = run[-1]
        #         next_leaf = abjad.inspect(last_leaf).leaf(1)
        #         abjad.attach(abjad.StopTextSpan(), next_leaf)
        #         abjad.attach(abjad.StopHairpin(), next_leaf)

        # for staff in abjad.iterate(self.score_template['Staff Group']).components(abjad.Staff):
        #     first_leaf = abjad.select(staff).leaves()[0]
        #     stop = abjad.LilyPondLiteral(r'\!', format_slot='after',)
        #     abjad.attach(stop, first_leaf)

        staffs = [
            staff
            for staff in abjad.iterate(self.score_template["Staff Group"]).components(
                abjad.Staff
            )
        ]

    def _adding_attachments(self):

        print("Adding attachments ...")
        bar_line = abjad.BarLine("||")
        metro = abjad.MetronomeMark((1, 4), (63, 72))

        markup2 = abjad.Markup(r"\bold { A }")
        mark2 = abjad.RehearsalMark(markup=markup2)

        markup3 = abjad.Markup(r"\bold { B }")
        mark3 = abjad.RehearsalMark(markup=markup3)

        markup4 = abjad.Markup(r"\bold { C }")
        mark4 = abjad.RehearsalMark(markup=markup4)

        markup5 = abjad.Markup(r"\bold { D }")
        mark5 = abjad.RehearsalMark(markup=markup5)

        instruments = evans.cyc(self.instruments)

        abbreviations = []
        abb = self.abbreviations
        mark_abbreviations = [abjad.Markup(_) for _ in abb]
        for x in mark_abbreviations:
            x.hcenter_in(12)
            abbreviations.append(abjad.MarginMarkup(markup=x))

        names = []
        nm = self.names
        mark_names = [abjad.Markup(_) for _ in nm]
        for x in mark_names:
            x.hcenter_in(14)
            names.append(abjad.StartMarkup(markup=x))

        # for staff in abjad.select(self.score_template['Staff Group']).components(abjad.Staff):
        #     last_leaf = abjad.select(staff).leaves()[-3]
        #     abjad.attach(bar_line, last_leaf)

        # for staff in abjad.iterate(self.score_template['Global Context']).components(abjad.Staff):
        #     leaf1 = abjad.select(staff).leaves()[0]
        # leaf2 = abjad.select(staff).leaves()[21]
        # leaf3 = abjad.select(staff).leaves()[27]
        # leaf4 = abjad.select(staff).leaves()[41]
        # leaf5 = abjad.select(staff).leaves()[56]
        # abjad.attach(metro, leaf1)
        # abjad.attach(mark2, leaf2)
        # abjad.attach(mark3, leaf3)
        # abjad.attach(mark4, leaf4)
        # abjad.attach(mark5, leaf5)

        # def _transposing_and_adding_clefs(self):

        print("transposing and adding clefs ...")
        for abbrev, name, inst, handler, voice in zip(
            abbreviations,
            names,
            self.instruments,
            self.clef_handlers,
            abjad.select(self.score_template["Staff Group"]).components(abjad.Voice),
        ):
            first_leaf = abjad.select(voice).leaves()[0]
            abjad.attach(abbrev, first_leaf, tag="applying staff names and clefs")
            abjad.attach(name, first_leaf, tag="applying staff names and clefs")
            abjad.attach(inst, first_leaf, tag="applying staff names and clefs")
            abjad.Instrument.transpose_from_sounding_pitch(voice)
            handler(voice)

        # print('Transforming Tuplet Brackets ...')
        # transformer = NoteheadBracketMaker()
        # transformer(self.score_template)

    def _render_file(self):
        score_file = abjad.LilyPondFile.new(
            self.score_template,
            includes=self.score_includes,
        )

        abjad.SegmentMaker.comment_measure_numbers(self.score_template)
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
        ###################
        directory = self.current_directory
        print("directory")
        print(directory)
        pdf_path = f"{directory}/illustration.pdf"
        print("path")
        print(pdf_path)
        path = pathlib.Path("illustration.pdf")
        if path.exists():
            print(f"Removing {pdf_path} ...")
            path.unlink()
        self.time_3 = time.time()
        print(f"Persisting {pdf_path} ...")
        result = abjad.persist(score_file).as_pdf(pdf_path, strict=79)  # or ly
        print(result[0])
        print(result[1])
        print(result[2])
        success = result[3]
        if success is False:
            print("LilyPond failed!")
        self.time_4 = time.time()
        abjad_time = self.time_4 - self.time_3
        print(f"Total time: {abjad_time} seconds")
        if path.exists():
            print(f"Opening {pdf_path} ...")
            os.system(f"open {pdf_path}")
        score_lines = open(f"{directory}/illustration.ly").readlines()
        build_path = (self.build_path / "score").resolve()
        open(f"{build_path}/{self.segment_name}.ly", "w").writelines(score_lines[15:-1])

        self.time_5 = time.time()

    def _extracting_parts(self):
        ###make parts###
        directory = self.current_directory
        for count, staff in enumerate(
            abjad.iterate(self.score_template).components(abjad.Voice)
        ):
            signatures = abjad.select(self.score_template["Global Context"]).components(
                abjad.Staff
            )
            signature_copy = abjad.mutate(signatures).copy()
            copied_staff = abjad.mutate(staff).copy()
            part = abjad.Score()
            part.insert(0, copied_staff)
            part.insert(0, signature_copy)
            part_file = abjad.LilyPondFile.new(
                part,
                includes=self.parts_includes,
            )
            pdf_path = f"{directory}/part_illustration{count + 1}.pdf"
            path = pathlib.Path(f"part_illustration{count + 1}.pdf")
            if path.exists():
                print(f"Removing {pdf_path} ...")
                path.unlink()
            print(f"Persisting {pdf_path} ...")
            result = abjad.persist(part_file).as_pdf(pdf_path, strict=79)
            print(result[0])
            print(result[1])
            print(result[2])
            success = result[3]
            if success is False:
                print("LilyPond failed!")
            if path.exists():
                print(f"Opening {pdf_path} ...")
                os.system(f"open {pdf_path}")
            build_path = (self.build_path / f"parts/part_{count + 1}").resolve()
            part_lines = open(
                f"{directory}/part_illustration{count + 1}.ly"
            ).readlines()
            open(f"{build_path}/{self.segment_name}.ly", "w").writelines(part_lines[15:-1])
        self.time_6 = time.time()

    def _write_optimization_log(self):
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
#     TimespanSpecifier,
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
