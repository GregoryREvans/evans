import datetime
import itertools
import os

import abjad

from . import consort
from .commands import HandlerCommand, RhythmCommand
from .sequence import flatten


class NoteheadBracketMaker(object):
    r"""
    Writes tuplet brackets with inserted note head.

    .. container:: example

        >>> tuplet = abjad.Tuplet((3, 2), "cs'8 d'8")
        >>> tuplet_2 = abjad.Tuplet((2, 3), components=[abjad.Note(0, (3, 8)), tuplet])
        >>> staff = abjad.Staff()
        >>> staff.append(tuplet_2)
        >>> new_brackets = evans.NoteheadBracketMaker()
        >>> b = new_brackets(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \tweak TupletNumber.text #(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text 3 2) "4")
                \times 2/3 {
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \tweak TupletNumber.text #(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text 2 3) "24")
                    \times 3/2 {
                        cs'8
                        d'8
                    }
                }
            }

    """

    def __call__(self, selections):
        return self._transform_brackets(selections)

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)

    def _transform_brackets(self, selections):
        for tuplet in abjad.select(selections).components(abjad.Tuplet):
            # written_duration = abjad.inspect(tuplet).duration().equal_or_greater_assignable
            time_duration = tuplet.multiplied_duration
            # print(time_duration)
            time_denominator = time_duration.denominator
            # print(time_denominator)
            imp_num, imp_den = tuplet.implied_prolation.pair
            # print(imp_num)
            notehead_wrapper = (
                time_denominator * imp_num
            )  # can't just be the denominator because something like 3/8 divided by 3 = 1/8 but just the denominator "8" doesn't give us enough information to go by
            multiplier = 1
            abjad.tweak(
                tuplet
            ).TupletNumber.text = f'#(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text {imp_den * multiplier} {imp_num * multiplier}) "{notehead_wrapper}")'
        return selections


class SegmentMaker(object):
    def __init__(
        self,
        abbreviations=None,
        add_final_grand_pause=True,
        barline="||",
        beam_pattern="runs",
        beam_rests=True,
        clef_handlers=None,
        colophon=None,
        commands=None,
        current_directory=None,
        cutaway=True,
        fermata="scripts.ushortfermata",
        instruments=None,
        names=None,
        name_staves=True,
        page_break_counts=None,
        rehearsal_mark=None,
        score_includes=None,
        score_template=None,
        segment_name=None,
        tempo=((1, 4), 90),
        time_signatures=None,
        tuplet_bracket_noteheads=True,
    ):
        self.abbreviations = abbreviations
        self.add_final_grand_pause = add_final_grand_pause
        self.barline = barline
        self.beam_pattern = beam_pattern
        self.beam_rests = beam_rests
        self.clef_handlers = clef_handlers
        self.colophon = colophon
        self.commands = commands
        self.current_directory = current_directory
        self.cutaway = cutaway
        self.fermata = fermata
        self.instruments = instruments
        self.names = names
        self.name_staves = name_staves
        self.page_break_counts = page_break_counts
        self.rehearsal_mark = rehearsal_mark
        self.score_includes = score_includes
        self.score_template = score_template
        self.segment_name = segment_name
        self.tempo = tempo
        self.time_signatures = time_signatures
        self.tuplet_bracket_noteheads = tuplet_bracket_noteheads

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)

    def _add_attachments(self):
        print("Adding attachments ...")
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
            abjad.iterpitches.transpose_from_sounding_pitch(voice)
            handler(voice)

    def _add_ending_skips(self):
        print("Adding ending skips ...")
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

    def beam_score(target):
        global_skips = [_ for _ in abjad.select(target["Global Context"]).leaves()]
        sigs = []
        for skip in global_skips:
            for indicator in abjad.inspect(skip).indicators():
                if isinstance(indicator, abjad.TimeSignature):
                    sigs.append(indicator)
        print("Beaming meter ...")
        for voice in abjad.iterate(target["Staff Group"]).components(abjad.Voice):
            for i, shard in enumerate(abjad.mutate(voice[:]).split(sigs)):
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
                        # include_rests=self.beam_rests,
                        include_rests=False,
                    )
                else:
                    beam_meter(
                        components=shard[:],
                        meter=met,
                        offset_depth=inventories[-2][0],
                        # include_rests=self.beam_rests,
                        include_rests=False,
                    )
        for trem in abjad.select(target).components(abjad.TremoloContainer):
            if abjad.StartBeam() in abjad.inspect(trem[0]).indicators():
                abjad.detach(abjad.StartBeam(), trem[0])
            if abjad.StopBeam() in abjad.inspect(trem[-1]).indicators():
                abjad.detach(abjad.StopBeam(), trem[-1])

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
            info_format = abjad.storage(info)
            string = f"import abjad\ninfo = {info_format}"
            fp.writelines(string)

    def _call_commands(self):
        if self.commands is None:
            return
        print("Calling commands ...")
        self.commands = flatten(self.commands)
        for group_type, group in itertools.groupby(self.commands, lambda _: type(_)):
            if group_type == RhythmCommand:
                rhythm_group = [_ for _ in group]
                self._make_containers(rhythm_group)
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
        handler_to_value = abjad.OrderedDict()
        voice_names = sorted(set(_.voice_name for _ in commands))
        command_groups = []
        for handler_type, command_group in itertools.groupby(
            commands, lambda _: type(_.handler)
        ):
            group = [_ for _ in command_group]
            command_groups.append(group)
        for group in command_groups:
            voice_collections = abjad.OrderedDict()
            global_collection = consort.LogicalTieCollection()
            for tie in abjad.select(
                self.score_template["Global Context"]
            ).logical_ties():
                global_collection.insert(tie)
            voice_collections["Global Context"] = global_collection
            for voice in abjad.select(self.score_template).components(abjad.Voice):
                collection = consort.LogicalTieCollection()
                for tie in abjad.select(voice).logical_ties():
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
                    handler = command.handler
                    handler(selection)
                    handler_to_value[handler.name] = handler.state()
        with open(f"{self.current_directory}/.handlers.py", "w") as fp:
            handler_to_value_format = abjad.storage(handler_to_value)
            string = f"import abjad\nhandler_to_value = {handler_to_value_format}"
            fp.writelines(string)

    def _extract_parts(self):
        print("Extracting parts ...")
        for count, voice in enumerate(
            abjad.iterate(self.score_template["Staff Group"]).components(abjad.Voice)
        ):
            t = r"\tag #'" + f"voice{count + 1}" + r" {"
            pre_lit = abjad.LilyPondLiteral(t, format_slot="absolute_before")
            post_lit = abjad.LilyPondLiteral(r"}", format_slot="absolute_after")
            abjad.attach(pre_lit, voice)
            abjad.attach(post_lit, voice)

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
        handler_to_value = abjad.OrderedDict()
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
            handler_to_value_format = abjad.storage(handler_to_value)
            string = f"import abjad\nhandler_to_value = {handler_to_value_format}"
            fp.writelines(string)

    def _make_mm_rests(self):
        print("Making MM rests ...")
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

    def _remove_final_grand_pause(self):
        if self.add_final_grand_pause is True:
            return
        print("Removing final grand pause ...")
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
        directory = self.current_directory
        pdf_path = abjad.Path(f"{directory}/illustration.pdf")
        if pdf_path.exists():
            pdf_path.unlink()
        print(f"Persisting {pdf_path.trim()} ...")
        result = abjad.persist(score_file).as_pdf(pdf_path, strict=79)
        success = result[3]
        if success is False:
            print("LilyPond failed!")
        if pdf_path.exists():
            print(f"Opening {pdf_path.trim()} ...")
            os.system(f"open {pdf_path}")
        with open(f"{directory}/illustration.ly") as pointer_1:
            score_lines = pointer_1.readlines()
            build_path = self.current_directory.parent.with_name("build")
            build_path /= "score"
            lines = score_lines[15:-1]
            with open(f"{build_path}/{self.segment_name}.ly", "w") as fp:
                fp.writelines(lines)

    def rewrite_meter(target):
        print("Rewriting meter ...")
        global_skips = [_ for _ in abjad.select(target["Global Context"]).leaves()]
        sigs = []
        for skip in global_skips:
            for indicator in abjad.inspect(skip).indicators():
                if isinstance(indicator, abjad.TimeSignature):
                    sigs.append(indicator)
        for voice in abjad.select(target["Staff Group"]).components(abjad.Voice):
            voice_dur = abjad.inspect(voice).duration()
            time_signatures = sigs[:-1]
            durations = [_.duration for _ in time_signatures]
            sig_dur = sum(durations)
            assert voice_dur == sig_dur, (voice_dur, sig_dur)
            shards = abjad.mutate(voice[:]).split(durations)
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

    def transform_brackets(target):
        print("Transforming brackets ...")
        for tuplet in abjad.select(target).components(abjad.Tuplet):
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
            if abjad.inspect(tuplet).sustained() is True:
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
                # if self.tuplet_bracket_noteheads is True:
                abjad.tweak(
                    tuplet
                ).TupletNumber.text = f'#(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text {imp_den * multiplier} {imp_num * multiplier}) "{notehead_wrapper}{dots}")'

    def _write_optimization_log(self):
        print("Writing optimization log ...")
        times = [self.pre_handlers_time + self.handlers_time + self.post_handlers_time]
        segment_time = sum(times)
        with open(f"{self.current_directory}/.optimization", "a") as fp:

            segment_time = f"Segment runtime: {segment_time} "
            segment_time += abjad.String("second").pluralize(segment_time)

            pre_handlers_time = f" Pre-handlers runtime: {self.pre_handlers_time} "
            pre_handlers_time += abjad.String("second").pluralize(
                self.pre_handlers_time
            )

            handlers_time = f" Handlers runtime: {self.handlers_time} "
            handlers_time += abjad.String("second").pluralize(self.handlers_time)

            post_handlers_time = f" Post-handlers runtime: {self.post_handlers_time} "
            post_handlers_time += abjad.String("second").pluralize(
                self.post_handlers_time
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

    def build_segment(self):
        with abjad.Timer() as timer:
            self._make_global_context()
        self.pre_handlers_time = int(timer.elapsed_time)
        with abjad.Timer() as timer:
            self._call_commands()
        self.handlers_time = int(timer.elapsed_time)
        with abjad.Timer() as timer:
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
        >>> for _ in [pre_tuplet_notes[:], tuplet, post_tuplet_notes[:]]:
        ...     staff.append(_)
        ...
        >>> evans.beam_meter(components=staff[:], meter=abjad.Meter((4, 4)), offset_depth=1)
        >>> abjad.show(staff) # doctest: +SKIP

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
                selector=abjad.select().leaves(grace=False),
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
                selector=abjad.select().leaves(grace=False),
            )
