"""
Command classes.
"""
import copy
import itertools
import random

import abjad
import baca
# import dataclasses
# import typing
import quicktions
from abjadext import rmakers

from .handlers import IntermittentVoiceHandler, RhythmHandler
from .quantizer import QSchemaTimeSignature, make_subdivided_music
from .rtm import RTMMaker, RTMTree, exponential_leaf_maker
from .select import get_top_level_components_from_leaves, select_all_but_final_leaf
from .sequence import CyclicList


class Command:
    def __init__(
        self,
        callable=None,
        command=None,
        contents=None,
        direction=None,
        indicator=None,
        selector=None,
        voice_name=None,
        source_voice_name=None,
        target_voice_name=None,
    ):
        self.callable = callable
        self.command = command
        self.contents = contents
        self.direction = direction
        self.indicator = indicator
        self.selector = selector
        self.voice_name = voice_name
        self.source_voice_name = source_voice_name
        self.target_voice_name = target_voice_name

    def __str__(self):
        return f"<{type(self).__name__}()>"
        # maybe use: black.format_str(?, mode=black.mode.Mode())

    def __repr__(self):
        return f"<{type(self).__name__}()>"

    def __call__(self, score):
        r"""
        Calls command on Score.

        .. container:: example

            >>> score = abjad.Score([abjad.Staff("c'4 c'4 c'4 c'4", name="staff one")])
            >>> def get_leaf_selector(context):
            ...     pitched_leaves = abjad.select.leaves(context, pitched=True)
            ...     get_leaves = abjad.select.get(pitched_leaves, [1])[0]
            ...     return get_leaves
            ...
            >>> command = evans.Command(
            ...     command="attach",
            ...     direction=abjad.UP,
            ...     indicator=abjad.Markup(r"\markup *"),
            ...     selector=get_leaf_selector,
            ...     voice_name="staff one"
            ... )
            ...
            >>> command(score)
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

                >>> print(abjad.lilypond(score))
                \new Score
                \with
                {
                    proportionalNotationDuration = #(ly:make-moment 1 25)
                }
                <<
                    \context Staff = "staff one"
                    {
                        c'4
                        c'4
                        ^ \markup *
                        c'4
                        c'4
                    }
                >>

        """
        if self.voice_name == "score":
            voice = score
            selection = score
        elif self.voice_name == "vertical":
            selection = self.selector(score["Staff Group"])
        else:
            try:
                voice = score[self.voice_name]
            except:  # what about staff?
                if "voice" in self.voice_name:
                    voice = [
                        _[:]
                        for _ in abjad.select.components(score, abjad.Voice)
                        if _.name == self.voice_name
                    ]
                if "staff" in self.voice_name:
                    voice = [
                        _[:]
                        for _ in abjad.select.components(score, abjad.Staff)
                        if _.name == self.voice_name
                    ]
            selection = self.selector(voice)
        if self.command == "attach":
            abjad.attach(self.indicator, selection, direction=self.direction)
        elif self.command == "call":
            self.callable(selection)
        elif self.command == "detach":
            abjad.detach(self.indicator, selection)
        elif self.command == "replace":
            self._replace(selection, self.contents, selection)
        elif self.command == "duplicate":
            selection[self.target_voice_name].extend(
                abjad.mutate.copy(selection[self.source_voice_name])
            )
        else:
            raise Exception(f"Invalid command {self.command}")

    def _replace(self, voice, contents, selection):
        abjad.mutate.replace(selection[:], contents[:])


def attach(voice_name, indicator, selector=None, direction=None):
    if selector is None:

        def selector(_):
            return abjad.select.leaf(_, 0)

    return Command(
        command="attach",
        direction=direction,
        indicator=indicator,
        selector=selector,
        voice_name=voice_name,
    )


def detach(voice_name, indicator, selector=None):
    if selector is None:

        def selector(_):
            return abjad.select.leaf(_, 0)

    return Command(
        command="detach",
        indicator=indicator,
        selector=selector,
        voice_name=voice_name,
    )


def replace(voice_name, contents, selector=None):
    if selector is None:

        def selector(_):
            return abjad.select.leaf(_, 0)

    return Command(
        command="replace",
        contents=contents,
        selector=selector,
        voice_name=voice_name,
    )


def call(voice_name, callable, selector=None):
    if selector is None:

        def selector(_):
            return abjad.select.leaf(_, 0)

    return Command(
        command="call",
        callable=callable,
        selector=selector,
        voice_name=voice_name,
    )


def duplicate(source_voice_name, target_voice_name):
    return Command(
        command="duplicate",
        voice_name="score",
        source_voice_name=source_voice_name,
        target_voice_name=target_voice_name,
    )


class HandlerCommand:
    def __init__(self, voice_name, timespan, handler):
        self.voice_name = voice_name
        self.timespan = timespan
        self.handler = handler

    def __str__(self):
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        return f"<{type(self).__name__}()>"


class Attachment:
    def __init__(
        self,
        indicator,
        selector=None,
        direction=None,
    ):
        self.indicator = indicator
        self.selector = selector
        self.direction = direction


class Callable:
    def __init__(
        self,
        callable,
        selector=None,
    ):
        self.callable = callable
        self.selector = selector


class MusicCommand:
    r"""
    evans.MusicCommand(
        ("Voice 1", (1, 3)),
        evans_rhythm_handler_builder(
            rhythm_handler,
            rest_selector,
        ),
        pitch_handler,
        evans.Attachment(
            abjad.Dynamic("p"),
            lambda _: abjad.select.leaf(_, 0, pitched=True),
        ),
        evans.attachment(
            abjad.Markup(r"\evans-custom-markup"),
            lambda _: abjad.select.leaf(_, 0, pitched=True),
            direction=abjad.UP,
        ),
        text_span_handler,
        preprocessor=evans.Sequence().fuse((1, 2))
    )
    """

    def __init__(
        self,
        location,
        *args,
        attachments=None,
        callables=None,
        preprocessor=None,
    ):
        self.location = location
        self.preprocessor = preprocessor
        self.attachments = []
        if attachments is not None:
            self.attachments = attachments
        self.callables = []
        if callables is not None:
            self.callables = callables
        self.threaded_commands = None

        for arg in args:
            if isinstance(arg, Attachment):
                self.attachments.append(arg)
            elif isinstance(arg, Callable):
                self.callables.append(arg)
            else:
                if not callable(arg):
                    if type(arg) == abjad.Articulation:

                        def selector(selections):
                            # runs = abjad.select.runs(selections)
                            run_ties = abjad.select.logical_ties(
                                selections, pitched=True
                            )
                            ties_first_leaves = [_[0] for _ in run_ties]
                            return ties_first_leaves

                    else:

                        def selector(_):
                            return abjad.select.leaf(_, 0, pitched=True)

                    new_attachment = Attachment(
                        arg,
                        selector,
                    )
                    self.attachments.append(new_attachment)
                elif callable(arg):
                    new_callable = Callable(
                        arg,
                        lambda _: abjad.select.leaves(_),
                    )
                    self.callables.append(new_callable)

        if isinstance(self.location, list):
            threaded_commands = []
            for location_ in self.location:
                new_command = type(self)(
                    location_,
                    attachments=self.attachments,
                    callables=self.callables,
                    preprocessor=self.preprocessor,
                )
                threaded_commands.append(new_command)
            self.threaded_commands = threaded_commands

    def __str__(self):
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        return f"<{type(self).__name__}()>"


def music(
    location,
    rmaker,
    *args,
    preprocessor=None,
    rewrite_meter=None,
):
    arguments = []
    for arg in args:
        arguments.append(arg)
    if rewrite_meter is not None:
        stack = [
            lambda _: rmakers.trivialize(abjad.select.tuplets(_)),
            lambda _: rmakers.rewrite_rest_filled(abjad.select.tuplets(_)),
            lambda _: rmakers.rewrite_sustained(abjad.select.tuplets(_)),
            lambda _: rmakers.extract_trivial(_),
            RewriteMeterCommand(boundary_depth=rewrite_meter),
        ]
        stack.extend(arguments)
    else:
        stack = [
            lambda _: rmakers.trivialize(abjad.select.tuplets(_)),
            lambda _: rmakers.rewrite_rest_filled(abjad.select.tuplets(_)),
            lambda _: rmakers.rewrite_sustained(abjad.select.tuplets(_)),
            lambda _: rmakers.extract_trivial(_),
        ]
        stack.extend(arguments)

    out = MusicCommand(
        location,
        rmaker,
        *stack,
        preprocessor=preprocessor,
    )
    return out


class RhythmCommand:
    def __init__(self, voice_name, timespan, handler):
        self.voice_name = voice_name
        self.timespan = timespan
        self.handler = handler

    def __str__(self):
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        return f"<{type(self).__name__}()>"


class Skeleton:
    def __init__(self, string, rewrite=False):
        self.selections = self.skeleton(string)
        self.rewrite = rewrite

    def __call__(self, durations):
        if abjad.get.duration(self.selections) == abjad.Duration(sum(durations)):
            if self.rewrite is True:
                for i, shard in enumerate(
                    abjad.select.partition_by_durations(self.selections, durations)
                ):
                    time_signature = durations[i]
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
            return self.selections
        else:
            message = (
                f"sel: {abjad.get.duration(self.selections)}, dur: {sum(durations)}"
            )
            raise Exception(message)

    @staticmethod
    def skeleton(argument):
        if isinstance(argument, str):
            string = f"{{ {argument} }}"
            container = abjad.parse(string)
            selection = abjad.mutate.eject_contents(container)
        elif isinstance(argument, list):
            selection = argument
        else:
            message = "evans.skeleton() accepts string or list of components,"
            message += " not {repr(argument)}."
            raise TypeError(message)
        return selection


# @dataclasses.dataclass(slots=True) # WARNING: does this break anything?
# WARNING: was class RewriteMeterCommand(rmakers.Command):
class RewriteMeterCommand:
    """
    Rewrite meter command.
    """

    def __init__(
        self,
        boundary_depth=None,
        reference_meters=(),
    ):
        self.boundary_depth = boundary_depth
        self.reference_meters = reference_meters

    def __post_init__(self):
        if self.boundary_depth is not None:
            assert isinstance(self.boundary_depth, int)
        self.reference_meters = tuple(self.reference_meters or ())
        if not all(isinstance(_, abjad.Meter) for _ in self.reference_meters):
            message = "must be sequence of meters:\n"
            message += f"   {repr(self.reference_meters)}"
            raise Exception(message)

    def __call__(self, voice, *, tag: abjad.Tag = abjad.Tag()) -> None:
        assert isinstance(voice, abjad.Voice), repr(voice)
        staff = abjad.get.parentage(voice).parent
        assert isinstance(staff, abjad.Staff), repr(staff)
        time_signature_voice = staff["TimeSignatureVoice"]
        assert isinstance(time_signature_voice, abjad.Voice)
        meters, preferred_meters = [], []
        for skip in time_signature_voice:
            time_signature = abjad.get.indicator(skip, abjad.TimeSignature)
            meter = abjad.Meter(time_signature)
            meters.append(meter)
        durations = [abjad.Duration(_) for _ in meters]
        reference_meters = self.reference_meters or ()
        non_tuplets = []
        for component in voice:
            if isinstance(component, abjad.Tuplet):
                new_dur = abjad.get.duration(component)
                new_mult = abjad.Multiplier(new_dur)
                new_skip = abjad.Skip((1, 1), multiplier=new_mult)
                non_tuplets.append(new_skip)
            else:
                non_tuplets.append(component)
        rmakers.split_measures(non_tuplets, durations=durations)
        selections = abjad.select.group_by_measure(voice[:])
        for meter, selection in zip(meters, selections):
            for reference_meter in reference_meters:
                if str(reference_meter) == str(meter):
                    meter = reference_meter
                    break
            preferred_meters.append(meter)
            nontupletted_leaves = []
            for leaf in abjad.iterate.leaves(selection):
                if not abjad.get.parentage(leaf).count(abjad.Tuplet):
                    nontupletted_leaves.append(leaf)
            rmakers.unbeam(nontupletted_leaves)
            abjad.Meter.rewrite_meter(
                selection,
                meter,
                boundary_depth=self.boundary_depth,
                rewrite_tuplets=False,
            )


def simple_hairpin(dynamics, *tweaks, selector):
    return lambda _: baca.hairpin(selector(_), dynamics)


def text_spanner(
    spanner_string, *tweaks, lilypond_id=None, bookend=None, selector=None
):
    if selector is not None:
        return lambda _: baca.text_spanner(
            selector(_),
            spanner_string,
            *tweaks,
            lilypond_id=lilypond_id,
            bookend=bookend,
        )
    else:
        return lambda _: baca.text_spanner(
            _, spanner_string, *tweaks, lilypond_id=lilypond_id, bookend=bookend
        )


def stack(
    rmaker, *args, preprocessor=None
):  # QUESTION: Is this an OK bridge in functionality? Imitating old?
    def returned_function(divisions):
        if preprocessor is not None:
            divisions = preprocessor(divisions)
        music = rmaker(divisions)
        container = abjad.Container(music)
        for arg in args:
            arg(container)
        music = abjad.mutate.eject_contents(container)
        return music

    return returned_function


def accelerando(
    *interpolations,
    previous_state=None,
    pre_commands=None,
    spelling=rmakers.Spelling(
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        increase_monotonic=False,
    ),
    state=None,
    tag=abjad.Tag(string=""),
    preprocessor=None,
    treat_tuplets=False,
):
    def returned_function(divisions, state=state, previous_state=previous_state):
        time_signatures = [_ for _ in divisions]
        if preprocessor is not None:
            durations = [abjad.Duration(_.pair) for _ in divisions]
            divisions = preprocessor(durations)
        nested_music = rmakers.accelerando(
            divisions,
            *interpolations,
            previous_state=previous_state,
            spelling=spelling,
            state=state,
            tag=tag,
        )
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        rmakers.duration_bracket(container)
        rmakers.feather_beam(container)
        music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def even_division(
    denominators,
    denominator="from_counts",
    *,
    extra_counts=(0,),
    pre_commands=None,
    previous_state=None,
    preprocessor=None,
    rewrite=None,
    treat_tuplets=True,
    spelling=rmakers.Spelling(
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        increase_monotonic=False,
    ),
    state=None,
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=state, previous_state=previous_state):
        time_signatures = [_ for _ in divisions]
        if preprocessor is not None:
            durations = [abjad.Duration(_.pair) for _ in divisions]
            divisions = preprocessor(durations)
        nested_music = rmakers.even_division(
            divisions,
            denominators=denominators,
            extra_counts=extra_counts,
            previous_state=previous_state,
            spelling=spelling,
            state=state,
            tag=tag,
        )
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        if rewrite is not None:
            meter_command = RewriteMeterCommand(boundary_depth=rewrite)
            metered_staff = rmakers.wrap_in_time_signature_staff(
                container[:], time_signatures
            )
            meter_command(metered_staff)
            music = abjad.mutate.eject_contents(metered_staff)
        else:
            music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def note(
    *,
    preprocessor=None,
    pre_commands=None,
    rewrite=None,
    treat_tuplets=True,
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=None, previous_state=None):
        time_signatures = [_ for _ in divisions]
        if preprocessor is not None:
            durations = [abjad.Duration(_.pair) for _ in divisions]
            divisions = preprocessor(durations)
        nested_music = rmakers.note(divisions)
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        if rewrite is not None:
            meter_command = RewriteMeterCommand(boundary_depth=rewrite)
            metered_staff = rmakers.wrap_in_time_signature_staff(
                container[:], time_signatures
            )
            meter_command(metered_staff)
            music = abjad.mutate.eject_contents(metered_staff)
        else:
            music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def multiplied_duration(
    written_duration=(1, 16),
    *,
    preprocessor=None,
    pre_commands=None,
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=None, previous_state=None):
        time_signatures = [_ for _ in divisions]
        if preprocessor is not None:
            durations = [abjad.Duration(_.pair) for _ in divisions]
            divisions = preprocessor(durations)
        nested_music = rmakers.multiplied_duration(divisions, duration=written_duration)
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def talea(
    counts,
    denominator,
    *,
    end_counts=(),
    extra_counts=(),
    preamble=(),
    previous_state=None,
    read_talea_once_only=False,
    pre_commands=None,
    preprocessor=None,
    rewrite=None,
    treat_tuplets=True,
    spelling=rmakers.Spelling(
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        increase_monotonic=False,
    ),
    state=None,
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=state, previous_state=previous_state):
        time_signatures = [_ for _ in divisions]
        if preprocessor is not None:
            durations = [abjad.Duration(_.pair) for _ in divisions]
            divisions = preprocessor(durations)
        nested_music = rmakers.talea(
            divisions,
            counts=counts,
            denominator=denominator,
            end_counts=end_counts,
            extra_counts=extra_counts,
            preamble=preamble,
            previous_state=previous_state,
            read_talea_once_only=read_talea_once_only,
            spelling=spelling,
            state=state,
            tag=tag,
        )
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        if rewrite is not None:
            meter_command = RewriteMeterCommand(boundary_depth=rewrite)
            metered_staff = rmakers.wrap_in_time_signature_staff(
                container[:], time_signatures
            )
            meter_command(metered_staff)
            music = abjad.mutate.eject_contents(metered_staff)
        else:
            music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def tuplet(
    tuplet_ratios,
    *,
    denominator=None,
    preprocessor=None,
    pre_commands=None,
    rewrite=None,
    treat_tuplets=True,
    spelling=rmakers.Spelling(
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        increase_monotonic=False,
    ),
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=None, previous_state=None):
        time_signatures = [_ for _ in divisions]
        if preprocessor is not None:
            durations = [abjad.Duration(_.pair) for _ in divisions]
            divisions = preprocessor(durations)
        nested_music = rmakers.tuplet(
            divisions=divisions,
            tuplet_ratios=tuplet_ratios,
            denominator=denominator,
            spelling=rmakers.Spelling(
                forbidden_note_duration=None,
                forbidden_rest_duration=None,
                increase_monotonic=False,
            ),
            tag=abjad.Tag(string=""),
        )
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        if rewrite is not None:
            meter_command = RewriteMeterCommand(boundary_depth=rewrite)
            metered_staff = rmakers.wrap_in_time_signature_staff(
                container[:], time_signatures
            )
            meter_command(metered_staff)
            music = abjad.mutate.eject_contents(metered_staff)
        else:
            music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def make_tied_notes(
    preprocessor=None, rewrite=False, treat_tuplets=True, pre_commands=None
):
    def handler_function(
        durations, state=None, previous_state=None
    ):  # seems to work accurately
        time_signatures = [_ for _ in durations]
        if preprocessor is not None:
            durations = preprocessor(durations)
        maker = rmakers.note
        nested_music = maker(durations)
        container = abjad.Container()
        for component in nested_music:
            container.extend(component)
        tie_target = select_all_but_final_leaf(container)
        rmakers.tie(tie_target)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        if rewrite is not None:
            meter_command = RewriteMeterCommand(boundary_depth=rewrite)
            metered_staff = rmakers.wrap_in_time_signature_staff(
                container[:], time_signatures
            )
            meter_command(metered_staff)
            music = abjad.mutate.eject_contents(metered_staff)
        else:
            music = abjad.mutate.eject_contents(container)

        return music

    return handler_function


def make_rtm(
    rtm,
    *,
    preprocessor=None,
    pre_commands=None,
    rewrite=None,
    treat_tuplets=True,
    intercept_irregular_meters=False,
):

    maker = RhythmHandler(
        RTMMaker(rtm, intercept_irregular_meters=intercept_irregular_meters),
        forget=False,
    )

    def returned_function(divisions, state=None, previous_state=None):
        time_signatures = [_ for _ in divisions]
        if preprocessor is not None:
            durations = [abjad.Duration(_.pair) for _ in divisions]
            divisions = preprocessor(durations)
        nested_music = maker(divisions)
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if pre_commands is not None:
            for pre_command in pre_commands:
                pre_command(container)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        if rewrite is not None:
            meter_command = RewriteMeterCommand(boundary_depth=rewrite)
            metered_staff = rmakers.wrap_in_time_signature_staff(
                container[:], time_signatures
            )
            meter_command(metered_staff)
            music = abjad.mutate.eject_contents(metered_staff)
        else:
            music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def slur(counts=None, cyclic=True, pitched=True, phrase=False, direction=None):
    def returned_function(selections):
        ties = abjad.select.logical_ties(selections, pitched=pitched)
        if counts is not None:
            groups = abjad.select.partition_by_counts(
                ties, counts, cyclic=cyclic, overhang=cyclic
            )
            for group in groups:
                if 1 < len(group):
                    if phrase is False:
                        abjad.slur(group, direction=direction)
                    else:
                        abjad.slur(
                            group,
                            start_slur=abjad.StartPhrasingSlur(),
                            stop_slur=abjad.StopPhrasingSlur(),
                            direction=direction,
                        )
        else:
            if phrase is False:
                abjad.slur(selections, direction=direction)
            else:
                abjad.slur(
                    selections,
                    start_slur=abjad.StartPhrasingSlur(),
                    stop_slur=abjad.StopPhrasingSlur(),
                    direction=direction,
                )

    return returned_function


def text_span(
    marks,
    style,
    counts=None,
    cyclic=True,
    pitched=True,
    padding=0,
    id=None,
    forget=False,
):
    cyclic_marks = CyclicList(marks, forget=forget)

    def returned_function(selections):
        ties = abjad.select.logical_ties(selections, pitched=pitched)
        if counts is not None:
            groups = abjad.select.partition_by_counts(
                ties, counts, cyclic=cyclic, overhang=cyclic
            )
        else:
            groups = [abjad.select.leaves(ties)]
        for group in groups:
            if 1 < len(group):
                if style[-1] == ">":
                    bookend = True
                    string = (
                        cyclic_marks(r=1)[0] + " " + style + " " + cyclic_marks(r=1)[0]
                    )
                else:
                    bookend = False
                    string = cyclic_marks(r=1)[0] + " " + style
                span = lambda _: baca.text_spanner(
                    _,
                    string,
                    abjad.Tweak(rf"- \tweak staff-padding {padding}"),
                    lilypond_id=id,
                    bookend=bookend,
                    pieces=lambda x: baca.select.lparts(x, [len(_), len(_) + 1]),
                )
                span(group)

    return returned_function


def bcp(bcps, padding=2):
    fractions = [_.split("/") for _ in bcps]
    bcps = [(int(_[0]), int(_[1])) for _ in fractions]

    def returned_function(selections):
        ties = abjad.select.logical_ties(selections, pitched=True)
        if 1 < len(ties[-1]):
            target = ties[-1][-2]
            abjad.detach(abjad.Tie(), target)
        baca.bcps(
            ties,
            bcps,
            abjad.Tweak(rf"- \tweak staff-padding {padding}"),
            bow_change_tweaks=(
                abjad.Tweak(r"- \tweak self-alignment-X #left"),
                abjad.Tweak(rf"- \tweak staff-padding {padding + 2}"),
            ),
        )

    return returned_function


def trill(
    counts=[1], cyclic=True, alteration=None, harmonic=False, padding=2, right_padding=0
):
    def returned_function(selections):
        ties = abjad.select.logical_ties(selections, pitched=True)
        if counts is not None:
            groups = abjad.select.partition_by_counts(
                ties, counts, cyclic=cyclic, overhang=cyclic
            )
            for group in groups:
                final = abjad.select.leaf(group, -1)
                next_leaf = abjad.get.leaf(final, 1)
                group.append(next_leaf)
            for group in groups:
                baca.trill_spanner(
                    group,
                    abjad.Tweak(rf"- \tweak staff-padding {padding}"),
                    abjad.Tweak(
                        rf"- \tweak bound-details.right.padding {right_padding}"
                    ),
                    alteration=alteration,
                    harmonic=harmonic,
                )

    return returned_function


def vibrato_spanner(
    peaks=[0, 1, 4, 2],
    wavelengths=[2],
    thickness=0.2,
    divisions=[4, 5],
    counts=[1],
    cyclic=True,
    padding=2,
    forget=False,
):
    cyc_peaks = CyclicList(peaks, forget=forget)
    cyc_divisions = CyclicList(divisions, forget=forget)
    cyc_wavelengths = CyclicList(wavelengths, forget=forget)

    def returned_function(selections):
        ties = abjad.select.logical_ties(selections, pitched=True)
        if counts is not None:
            groups = abjad.select.partition_by_counts(
                ties, counts, cyclic=cyclic, overhang=cyclic
            )
            for group in groups:
                final = abjad.select.leaf(group, -1)
                next_leaf = abjad.get.leaf(final, 1)
                group.append(next_leaf)
            for group in groups:
                current_wavelength = cyc_wavelengths(r=1)[0]
                current_divisions = cyc_divisions(r=1)[0]
                current_peaks = str(tuple(cyc_peaks(r=current_divisions)))
                current_peaks = current_peaks.replace(",", "")
                baca.trill_spanner(
                    group,
                    abjad.Tweak(rf"- \tweak staff-padding {padding}"),
                    # abjad.Tweak(fr"- \tweak bound-details.right.padding 10"),
                )
                vib_literal = abjad.LilyPondLiteral(
                    rf"\vibrato #'{current_peaks} #{current_wavelength} #{thickness}",
                    site="before",
                )
                abjad.attach(vib_literal, abjad.select.leaf(group, 0))

    return returned_function


def hairpin(
    dynamics,
    counts=None,
    cyclic=True,
    pitched=True,
    final_hairpin=False,
    remove_length_1_spanner_start=False,
):
    def returned_function(selections):
        def selector(selections_):
            ties = abjad.select.logical_ties(selections_, pitched=pitched)
            if counts is not None:
                counts_ = [_ - 1 for _ in counts]
                groups = abjad.select.partition_by_counts(
                    ties, counts_, cyclic=cyclic, overhang=cyclic
                )
            else:
                groups = [abjad.select.leaves(ties)]
            return groups

        baca.hairpin(
            selections,
            dynamics,
            pieces=selector,
            final_hairpin=final_hairpin,
            remove_length_1_spanner_start=remove_length_1_spanner_start,
        )

    return returned_function


def sustain_pedal(
    counts=None,
    cyclic=True,
    pitched=True,
    alternating=False,
    lifts=False,
):
    def returned_function(selections):
        def selector(selections_):
            ties = abjad.select.logical_ties(selections_, pitched=pitched)
            if counts is not None:
                counts_ = [_ - 1 for _ in counts]
                groups = abjad.select.partition_by_counts(
                    ties, counts_, cyclic=cyclic, overhang=cyclic
                )
            else:
                groups = [abjad.select.leaves(ties)]
            return groups

        groups = selector(selections)
        for i, group in enumerate(groups):
            if alternating is True:
                if i % 2 == 0 and i != 0:
                    continue
            if lifts is True:
                if 0 < i:
                    first_leaf = abjad.select.leaf(group, 0)
                    previous_leaf = abjad.get.leaf(first_leaf, -1)
                    lift_group = [previous_leaf]
                    lift_group.extend(group)
                    baca.sustain_pedal(lift_group)
                else:
                    baca.sustain_pedal(group)
            else:
                baca.sustain_pedal(group)

    return returned_function


def figure(
    collections,
    counts,
    denominator,
    *,
    acciaccatura=None,
    affix=None,
    restart_talea=False,
    tsd=None,
    spelling=None,
    treatments=(),
):
    container = baca.figure(
        collections=collections,
        counts=counts,
        denominator=denominator,
        acciaccatura=acciaccatura,
        affix=affix,
        restart_talea=restart_talea,
        tsd=tsd,
        spelling=spelling,
        treatments=treatments,
    )
    # raise Exception([_ for _ in abjad.select.components(container, abjad.Container)[1:]])
    selections = [_ for _ in abjad.select.components(container, abjad.Container)[1:]]

    return selections


def _do_indexed_imbrication(
    container: abjad.Container,
    segment: list,
    voice_name: str,
    *commands,
    cyclic_period=None,
    hocket: bool = False,
    truncate_ties: bool = False,
) -> dict[str, list]:
    original_container = container
    container = copy.deepcopy(container)
    abjad.override(container).TupletBracket.stencil = False
    abjad.override(container).TupletNumber.stencil = False
    segment = abjad.sequence.flatten(segment, depth=-1)
    original_logical_ties = abjad.select.logical_ties(original_container)
    logical_ties = abjad.select.logical_ties(container)
    pairs = zip(logical_ties, original_logical_ties)
    relevant_ties = abjad.select.get(logical_ties, segment, period=cyclic_period)
    for logical_tie, original_logical_tie in pairs:
        if isinstance(logical_tie.head, abjad.Rest):
            for leaf in logical_tie:
                duration = leaf.written_duration
                skip = abjad.Skip(duration)
                abjad.mutate.replace(leaf, [skip])
        elif isinstance(logical_tie.head, abjad.Skip):
            pass
        elif logical_tie in relevant_ties:
            baca.figures._trim_matching_chord(logical_tie, logical_tie[0].written_pitch)
            if truncate_ties:
                head = logical_tie.head
                tail = logical_tie.tail
                for leaf in logical_tie[1:]:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate.replace(leaf, [skip])
                abjad.detach(abjad.Tie, head)
                next_leaf = abjad.get.leaf(tail, 1)
                if next_leaf is not None:
                    abjad.detach(abjad.RepeatTie, next_leaf)
            if hocket:
                for leaf in original_logical_tie:
                    indicators = abjad.get.indicators(leaf)
                    for indicator in indicators:
                        abjad.detach(indicator, leaf)
                    duration = leaf.written_duration
                    skip = abjad.Rest(duration)
                    literal = abjad.LilyPondLiteral(
                        [
                            r"\once \override Voice.Stem.stemlet-length = #0",
                            r"\once \hide Voice.Rest",
                        ],
                        site="before",
                    )
                    abjad.attach(literal, skip)
                    for indicator in indicators:
                        abjad.attach(indicator, skip)
                    abjad.mutate.replace(leaf, [skip])
        else:
            for leaf in logical_tie:
                duration = leaf.written_duration
                skip = abjad.Skip(duration)
                abjad.mutate.replace(leaf, [skip])
    for command in commands:
        command(container)
    selection = [container]
    if not hocket:
        pleaves = baca.select.pleaves(container)
        assert isinstance(pleaves, list)
        for pleaf in pleaves:
            abjad.attach(baca.enums.ALLOW_OCTAVE, pleaf)
    return {voice_name: selection}


def imbricate(
    selections,
    pitches,
    name,
    *,
    direction=abjad.UP,
    articulation=None,
    beam=False,
    secondary=False,
    allow_unused_pitches=False,
    by_pitch_class=False,
    by_index=False,
    cyclic_period=None,
    hocket=False,
    truncate_ties=False,
    direct_attachments=False,
    note_head=None,
):
    def _find_parent(selections):
        first_leaf = abjad.select.leaf(selections, 0)
        parentage = abjad.get.parentage(first_leaf)
        parent_voice = abjad.select.components(parentage, abjad.Voice)
        return f"{parent_voice[0].name} temp"

    attachment_direction = None
    if direct_attachments is True:
        attachment_direction = direction
    container = abjad.Container(simultaneous=True)
    original_voice = abjad.Voice(name=_find_parent(selections))
    intermittent_voice = abjad.Voice(name=name)
    selections_ = get_top_level_components_from_leaves(selections)
    abjad.mutate.wrap(selections_, original_voice)
    abjad.mutate.wrap(original_voice, container)
    if beam is True:
        groups = rmakers.nongrace_leaves_in_each_tuplet(original_voice)
        rmakers.beam_groups(groups)
        baca.extend_beam(abjad.select.leaf(original_voice, -1))

    if by_index is False:
        imbrications = baca.imbricate(
            original_voice,
            "v1",
            pitches,
            allow_unused_pitches=allow_unused_pitches,
            by_pitch_class=by_pitch_class,
            hocket=hocket,
            truncate_ties=truncate_ties,
        )
    else:
        imbrications = _do_indexed_imbrication(
            container=original_voice,
            voice_name="v1",
            segment=pitches,
            hocket=hocket,
            truncate_ties=truncate_ties,
            cyclic_period=cyclic_period,
        )
    imbrication = imbrications["v1"][0]
    contents = abjad.mutate.eject_contents(imbrication)
    intermittent_voice.extend(contents)
    if note_head is not None:
        for tie in abjad.select.logical_ties(intermittent_voice, pitched=True):
            start_literal = abjad.LilyPondLiteral(note_head, site="before")
            stop_literal = abjad.LilyPondLiteral(r"\revert-noteheads", site="after")
            abjad.attach(start_literal, tie[0])
            abjad.attach(stop_literal, tie[-1])

    groups = rmakers.nongrace_leaves_in_each_tuplet(intermittent_voice)
    rmakers.beam_groups(groups, beam_rests=True)
    if articulation is not None:
        for head in baca.select.pheads(intermittent_voice):
            if isinstance(articulation, str):
                abjad.attach(
                    abjad.Articulation(articulation),
                    head,
                    direction=attachment_direction,
                )
            else:
                abjad.attach(articulation, head, direction=attachment_direction)
    baca.extend_beam(abjad.select.leaf(intermittent_voice, -1))
    abjad.override(intermittent_voice).TupletBracket.stencil = False
    abjad.override(intermittent_voice).TupletNumber.stencil = False

    container.append(intermittent_voice)
    if secondary is False:
        direction_1 = "One"
        direction_2 = "Two"
    else:
        direction_1 = "Three \shiftOff"
        direction_2 = "Four \shiftOff"
    if direction == abjad.UP:
        abjad.attach(
            abjad.LilyPondLiteral(rf"\voice{direction_2}", site="before"),
            abjad.select.leaf(original_voice, 0),
        )
        abjad.attach(
            abjad.LilyPondLiteral(rf"\voice{direction_1}", site="before"),
            abjad.select.leaf(intermittent_voice, 0),
        )
    else:
        abjad.attach(
            abjad.LilyPondLiteral(rf"\voice{direction_1}", site="before"),
            abjad.select.leaf(original_voice, 0),
        )
        abjad.attach(
            abjad.LilyPondLiteral(rf"\voice{direction_2}", site="before"),
            abjad.select.leaf(intermittent_voice, 0),
        )
    closing_literal = abjad.LilyPondLiteral(r"\oneVoice", site="after")
    abjad.attach(closing_literal, container)


def auto_staff_change(upper_staff_name, lower_staff_name):
    def returned_function(selections):
        def up_or_down(pitch, first=False):
            numbered_pitch = abjad.NumberedPitch(pitch)
            if 0 < numbered_pitch:
                return "UP"
            elif numbered_pitch < 0:
                return "DOWN"
            else:
                if first is False:
                    return None
                else:
                    return "UP"

        ties = abjad.select.logical_ties(selections, pitched=True)
        active_staff = up_or_down(ties[0][0].written_pitch, first=True)
        up_literal = abjad.LilyPondLiteral(
            rf'\change Staff = "{upper_staff_name}"', site="before"
        )
        down_literal = abjad.LilyPondLiteral(
            rf'\change Staff = "{lower_staff_name}"', site="before"
        )
        if active_staff == "UP":
            abjad.attach(up_literal, ties[0][0])
        else:
            abjad.attach(down_literal, ties[0][0])

        for tie in ties[1:]:
            desired_staff = up_or_down(tie[0].written_pitch)
            if desired_staff is None:
                continue
            elif desired_staff == active_staff:
                continue
            elif desired_staff == "UP":
                abjad.attach(up_literal, tie[0])
            elif desired_staff == "DOWN":
                abjad.attach(down_literal, tie[0])
            else:
                raise Exception("BAD TESTER RESULT")
            active_staff = desired_staff

    return returned_function


def replace_rests_with_skips(selections):
    skips = []
    rests = abjad.select.leaves(selections, pitched=False)
    for rest in rests:
        duration = rest.written_duration
        s = abjad.Skip(duration)
        skips.append(s)
    abjad.mutate.replace(rests, skips)


def make_anchor_skips_from_voices(
    *args, name="anchor voice", destination="voice 1", exclude_final_measure=True
):
    input = [_ for _ in args]
    voices = abjad.select.components(input, abjad.Voice)
    if exclude_final_measure is True:
        for voice in voices:
            if voice.name == destination:
                measures = abjad.select.group_by_measure(voice)
                final_measure = measures[-1]
                final_timespan = abjad.get.timespan(final_measure)

    leaves = abjad.select.leaves(voices)
    timespans = [abjad.get.timespan(leaf) for leaf in leaves]
    timespans.sort()
    out_spans = [timespans[0]]
    for span in timespans[1:]:
        if span.start_offset == out_spans[-1].start_offset:
            continue
        if span.start_offset < out_spans[-1].stop_offset:
            out_spans[-1].stop_offset = span.start_offset
        out_spans.append(span)
    out_spans = abjad.TimespanList(out_spans)
    if exclude_final_measure is True:
        out_spans = out_spans - final_timespan
    out_durations = [_.duration for _ in out_spans]
    nested_music = rmakers.multiplied_duration(out_durations, abjad.Skip)
    container = abjad.Container()
    for component in nested_music:
        if isinstance(component, list):
            container.extend(component)
        else:
            container.append(component)
    music = abjad.mutate.eject_contents(container)

    destination = [_ for _ in voices if _.name == destination][0]
    if exclude_final_measure is True:
        measures = abjad.select.group_by_measure(destination)[:-1]
        destination = []
        for measure in measures:
            destination.extend(measure)

    handler = IntermittentVoiceHandler(
        music,
        direction="neutral",
        from_components=True,
        voice_name=name,
    )

    handler(destination)


def wrap_in_repeats(selections, number_of_repeats=2, barline_color="black"):
    leaves = abjad.select.leaves(selections)
    abjad.attach(
        abjad.LilyPondLiteral(
            rf'\repeatBracket {number_of_repeats} "{barline_color}" {{ ', site="before"
        ),
        leaves[0],
    )
    abjad.attach(
        abjad.LilyPondLiteral("}", site="after"),
        leaves[-1],
    )
    # abjad.LilyPondLiteral(r"""\set Score.repeatCommands = #'((volta "1-2"))""", site="before")
    # abjad.LilyPondLiteral(
    #     r"""\set Score.repeatCommands = #'((volta #f) (volta "3"))""",
    #     site="before",
    # )
    # abjad.LilyPondLiteral(
    #     r"""\set Score.repeatCommands = #'((volta #f))""",
    #     site="before",
    # )


def do_fitted_obgc(
    target,
    number_of_leaves=[5],
    *,
    # voice_name="obgc",
    accelerando_switch_indices=None,
    accelerando_written_durations=[32],
    anchor_voice_number=2,
    beam_position=6,
    do_not_beam=False,
    do_not_slur=False,
    feathered=False,
    fixed_gettato_pitch=None,
    font_size=-4,
    gettato=False,
    grace_voice_number=1,
    grow_directions=None,
    interval_of_transposition="+P8",
    over_figure=False,
    portion_of_total_duration=None,
    with_beam_nibs=False,
    written_duration=8,
):
    if portion_of_total_duration is not None:
        portion_of_total_duration = quicktions.Fraction(
            portion_of_total_duration[0], portion_of_total_duration[1]
        )
    cyc_accel_written_durs = CyclicList(accelerando_written_durations, forget=False)
    if grow_directions is not None:
        cyc_grow_dirs = CyclicList(grow_directions, forget=False)
    if accelerando_switch_indices is not None:
        cyc_accel_switch_ind = CyclicList(accelerando_switch_indices, forget=False)
    else:
        cyc_accel_switch_ind = CyclicList([None], forget=False)
    group_numbers = CyclicList(number_of_leaves, forget=False)
    number_of_leaves = CyclicList(number_of_leaves, forget=False)
    if over_figure is True:
        duration = abjad.get.duration(target)
        durations = [duration]
        targets = [target[:]]
    else:
        ties = abjad.select.logical_ties(target, pitched=True)
        durations = [abjad.get.duration(tie) for tie in ties]
        targets = ties
    for target_, duration in zip(targets, durations):
        n_of_l = number_of_leaves(r=1)[0]
        if gettato is True:
            first_leaf = abjad.select.leaf(target_, 0)
            if isinstance(first_leaf, abjad.Note):
                pitch = first_leaf.written_pitch
            elif isinstance(first_leaf, abjad.Chord):
                pitch = first_leaf.written_pitches[-1]
        else:
            pitch = "c'"
        if grow_directions is not None:
            next_dur = cyc_accel_written_durs(r=1)[0]
            next_grow_dir = cyc_grow_dirs(r=1)
            next_switch_ind = cyc_accel_switch_ind(r=1)
            content_maker = exponential_leaf_maker(
                [(1, next_dur)],
                number_of_leaves.lst,
                next_grow_dir,
                next_switch_ind,
            )
            contents = content_maker([duration])
        else:
            contents = [
                abjad.Note(pitch, abjad.Duration(1, written_duration))
                for _ in range(n_of_l)
            ]
        if grow_directions is None:
            calculated_duration = duration / n_of_l
            if portion_of_total_duration is not None:
                calculated_duration = calculated_duration * portion_of_total_duration
        else:
            calculated_duration = portion_of_total_duration
        new_container = abjad.on_beat_grace_container(
            contents,
            target_,
            anchor_voice_number=anchor_voice_number,
            leaf_duration=calculated_duration,
            do_not_slash=True,
            do_not_slur=do_not_slur,
            do_not_beam=do_not_beam,
            font_size=font_size,
            grace_voice_number=grace_voice_number,
        )
        if gettato is False:
            abjad.override(target_[0]).NoteHead.layer = 3
            abjad.override(
                new_container[0]
            ).Beam.positions = rf"#'({beam_position} . {beam_position})"
            tweak_literal = abjad.LilyPondLiteral(
                rf"\once \override Slur.details.region-size = #{beam_position + 0.5}",
                site="before",
            )
            abjad.attach(tweak_literal, new_container[0])
            abjad.override(
                new_container[0]
            ).Slur.positions = rf"#'({beam_position + 0.5} . {beam_position + 0.5})"
            start_scheme_literal = abjad.LilyPondLiteral(
                r"\start-ob-multi-grace", site="before"
            )
            abjad.attach(start_scheme_literal, new_container[0])
            stop_scheme_literal = abjad.LilyPondLiteral(
                r"\stop-ob-multi-grace", site="after"
            )
            abjad.attach(stop_scheme_literal, new_container[-1])
        if gettato is True:
            graces = abjad.select.leaves(new_container, pitched=True, grace=True)
            groups = abjad.select.group_by_contiguity(graces)
            for group in groups:
                group_number = group_numbers(r=1)[0]
                abjad.attach(
                    abjad.Markup(rf'\markup {{\hspace #1 "gett.({group_number})" }}'),
                    group[0],
                )
                start_literal = abjad.LilyPondLiteral(
                    [
                        r"\override NoteHead.no-ledgers = ##t",
                        r"\override Accidental.transparent = ##t",
                        r"\override NoteHead.transparent = ##t",
                        # r"\override NoteHead.X-extent = #'(0 . 0)",
                    ],
                    site="before",
                )
                abjad.attach(start_literal, group[0])
                stop_literal = abjad.LilyPondLiteral(
                    [
                        r"\override NoteHead.no-ledgers = ##f",
                        r"\override Accidental.transparent = ##f",
                        r"\override NoteHead.transparent = ##f",
                        # r"\revert NoteHead.X-extent",
                    ],
                    site="after",
                )
                abjad.attach(stop_literal, group[-1])
                if with_beam_nibs is not False:
                    if written_duration == 8:
                        beam_count = abjad.BeamCount(1, 1)
                    elif written_duration == 16:
                        beam_count = abjad.BeamCount(2, 2)
                    elif written_duration == 32:
                        beam_count = abjad.BeamCount(3, 3)
                    elif written_duration == 64:
                        beam_count = abjad.BeamCount(4, 4)
                    else:
                        raise Exception(
                            f"INCOMPATIBLE WRITTEN DURATION: {written_duration}"
                        )
                    if with_beam_nibs != "trailing":
                        abjad.attach(beam_count, group[0])
                    abjad.attach(beam_count, group[-1])
                if feathered is True:
                    literal = abjad.LilyPondLiteral(
                        r"\once \override Beam.grow-direction = #left",
                        site="before",
                    )
                    abjad.attach(literal, group[0])
            for grace in graces:
                if fixed_gettato_pitch is None:
                    interval = abjad.NamedInterval(interval_of_transposition)
                    new_note = interval.transpose(grace)
                else:
                    new_note = abjad.Note(fixed_gettato_pitch, abjad.Duration(1, 4))
                if isinstance(grace, abjad.Note):
                    grace.written_pitch = new_note.written_pitch
                abjad.attach(abjad.Articulation("staccato"), grace, direction=abjad.UP)


def fitted_obgc(
    # voice_name="obgc",
    accelerando_switch_indices=None,
    accelerando_written_durations=[32],
    anchor_voice_number=2,
    beam_position=6,
    do_not_beam=False,
    do_not_slur=False,
    feathered=False,
    fixed_gettato_pitch=None,
    font_size=-4,
    gettato=False,
    grace_voice_number=1,
    grow_directions=None,
    interval_of_transposition="+P8",
    number_of_leaves=[5],
    over_figure=False,
    portion_of_total_duration=None,
    with_beam_nibs=False,
    written_duration=8,
):
    f = lambda selections: do_fitted_obgc(
        selections,
        number_of_leaves=number_of_leaves,
        anchor_voice_number=anchor_voice_number,
        beam_position=beam_position,
        over_figure=over_figure,
        written_duration=written_duration,
        gettato=gettato,
        grace_voice_number=grace_voice_number,
        with_beam_nibs=with_beam_nibs,
        feathered=feathered,
        interval_of_transposition=interval_of_transposition,
        fixed_gettato_pitch=fixed_gettato_pitch,
        do_not_slur=do_not_slur,
        do_not_beam=do_not_beam,
        font_size=font_size,
        accelerando_written_durations=accelerando_written_durations,
        grow_directions=grow_directions,
        accelerando_switch_indices=accelerando_switch_indices,
        portion_of_total_duration=portion_of_total_duration,
    )
    return f


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


def long_beam(
    selections,
    stemlet_length=None,
    beam_rests=True,
    beam_lone_notes=False,
    direction=abjad.UP,
):
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
                direction=direction,
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


def subdivided_ties(
    *args,
    source_maker=rmakers.note,
    search_tree=None,
    treat_tuplets=False,
):
    args_count = 0
    for arg in args:
        args_count += 1

    def returned_function(
        divisions, state=None, previous_state=None, search_tree=search_tree
    ):
        source_leaves = source_maker(divisions)
        source_container = abjad.Container(source_leaves)
        if 0 < args_count:
            args_ = []
            schema_list = []
            represented_schema_indices = []
            for arg in args:
                if isinstance(arg, QSchemaTimeSignature):
                    schema_list.append(arg)
                    represented_schema_indices.append(arg.index)
                else:
                    args_.append(arg)
            for i, division in enumerate(divisions):
                if i not in represented_schema_indices:
                    schema = QSchemaTimeSignature(
                        index=i,
                        time_signature=division,
                        use_full_measure=True,
                    )
                    schema_list.append(schema)
            new_args = args_ + schema_list
            nested_music = make_subdivided_music(
                *new_args, ties=source_container, search_tree=search_tree
            )  # ties?
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
        else:
            music = abjad.mutate.eject_contents(source_container)
        # print(music, "\r")
        return music

    return returned_function


def wrap_in_cross_staff(selections):
    start_literal = abjad.LilyPondLiteral(r"\crossStaff {", site="before")
    stop_literal = abjad.LilyPondLiteral(r"}", site="after")
    abjad.attach(start_literal, abjad.select.leaf(selections, 0))
    abjad.attach(stop_literal, abjad.select.leaf(selections, -1))


def find_cross_staff_events(selections, comparison):
    crossable = []
    comparison_ties = abjad.select.logical_ties(comparison, pitched=True)
    comparison_start_offsets = [
        abjad.get.timespan(_).start_offset for _ in comparison_ties
    ]
    for tie in abjad.select.logical_ties(selections, pitched=True):
        if abjad.get.timespan(tie).start_offset in comparison_start_offsets:
            crossable.append(tie)
    for tie in crossable:
        wrap_in_cross_staff(tie)


def cross_staff(target, reference_name, reference_selector):
    score = abjad.get.parentage(target[0])[-1]
    reference_target = score[reference_name]
    reference_selections = reference_selector(reference_target)
    find_cross_staff_events(target, reference_selections)


def cross_staff_copy(
    target, reference_name, reference_selector, reference_indices, indices_period=None
):
    score = abjad.get.parentage(target[0])[-1]
    reference_target = score[reference_name]
    reference_selections = reference_selector(reference_target)
    reference_selections = abjad.select.logical_ties(reference_selections, pitched=True)
    ties = abjad.select.get(reference_selections, reference_indices, indices_period)
    out = []
    for tie in reference_selections:
        if tie in ties:
            new_leaf = rmakers.multiplied_duration(
                [abjad.get.duration(tie)], duration=(1, 8)
            )
            out.extend(new_leaf)
        else:
            new_leaf = rmakers.multiplied_duration(
                [abjad.get.duration(tie)], abjad.Skip
            )
            out.extend(new_leaf)
    for tie in abjad.select.logical_ties(out, pitched=True):
        start_literal = abjad.LilyPondLiteral(r"\crossStaff {", site="before")
        stop_literal = abjad.LilyPondLiteral(r"}", site="after")
        abjad.attach(start_literal, tie[0])
        abjad.attach(stop_literal, tie[-1])
    abjad.mutate.replace(target, out)


def unsichtbare_farben(
    subdivisions_range=(1, 7),
    proportions_range=(1, 12),
    reproportioning_range=(1, 4),
    motives_per_figure_range=(1, 5),
    number_of_voices=6,
    measurewise_voice_indices=[0],
    cyclic_voice_indices=False,
    proportions_from_combinations=False,
    subdivide_both_proportions=False,
    reverse_proportions=False,
    seed=1,
    preprocessor=None,
    rewrite=None,
    treat_tuplets=True,
):
    random.seed(seed)
    subdivisions = [_ for _ in range(subdivisions_range[0], subdivisions_range[1])]
    proportions = [_ for _ in range(proportions_range[0], proportions_range[1])]
    motives_per_figure = [
        _ for _ in range(motives_per_figure_range[0], motives_per_figure_range[1])
    ]
    re_proportions = [
        _ for _ in range(reproportioning_range[0], reproportioning_range[1])
    ]

    if proportions_from_combinations is False:
        if reverse_proportions is True:
            proportion_pairs = [(proportions[0], _) for _ in proportions]
        else:
            proportion_pairs = [(_, proportions[0]) for _ in proportions]
    else:
        proportion_pairs = []
        combinations = itertools.combinations_with_replacement(proportions, 2)
        for combination in combinations:
            if (
                proportions_range[1] < combination[0]
                and combination[0] == combination[1]
            ):
                continue
            else:
                proportion_pairs.append(combination)
    subdivided_pairs = []
    if subdivide_both_proportions is False:
        for pair in proportion_pairs:
            for subdivision in subdivisions:
                proportion = random.choice(re_proportions)
                if 1 < subdivision:
                    temp_tree = RTMTree(
                        [pair[0], [pair[1], [1 for _ in range(subdivision)]]],
                        size=proportion,
                    )
                    reversed_tree = RTMTree(
                        [[pair[1], [1 for _ in range(subdivision)]], pair[0]],
                        size=proportion,
                    )
                else:
                    temp_tree = RTMTree([pair[0], pair[1]], size=proportion)
                    reversed_tree = RTMTree([pair[1], pair[0]], size=proportion)
                subdivided_pairs.append(temp_tree)
                subdivided_pairs.append(reversed_tree)
    else:
        combinations = itertools.combinations_with_replacement(subdivisions, 2)
        for pair in proportion_pairs:
            for combination in combinations:
                proportion = random.choice(re_proportions)
                temp_tree = RTMTree(
                    [
                        [pair[0], [1 for _ in range(combination[0])]],
                        [pair[1], [1 for _ in range(combination[1])]],
                    ],
                    size=proportion,
                )
                subdivided_pairs.append(temp_tree)

    def returned_function(
        durations,
        state=None,
        previous_state=None,
        measurewise_voice_indices=measurewise_voice_indices,
    ):
        random.seed(seed)
        time_signatures = [_ for _ in durations]
        if preprocessor is not None:
            durations = preprocessor(durations)
        size = len(durations)
        if cyclic_voice_indices is True:
            measurewise_voice_indices = CyclicList(
                measurewise_voice_indices, forget=False
            )
            measurewise_voice_indices = measurewise_voice_indices(r=size)
        else:
            while len(measurewise_voice_indices) < size:
                measurewise_voice_indices.append(measurewise_voice_indices[-1])
            if size < len(measurewise_voice_indices):
                measurewise_voice_indices = measurewise_voice_indices[:size]
        voices = []
        for i in range(number_of_voices):
            voice = []
            for division in durations:
                number_of_figures = random.choice(motives_per_figure)
                figures = []
                for opportunity in range(number_of_figures):
                    chosen = random.choice(subdivided_pairs)
                    figures.append(chosen)
                voice.append(RTMTree(figures))
            voices.append(voice)
        final_conjoint_layer = []
        for i, dur_ in enumerate(durations):
            chosen_voice = voices[measurewise_voice_indices[i]]
            chosen_gesture = chosen_voice[i]
            final_conjoint_layer.append(str(chosen_gesture))
        # for _ in final_conjoint_layer:
        #     print(_, "\n")
        maker = RTMMaker(final_conjoint_layer)
        nested_music = maker(durations)
        container = abjad.Container()
        for component in nested_music:
            if isinstance(component, list):
                container.extend(component)
            else:
                container.append(component)
        if treat_tuplets is True:
            command_target = abjad.select.tuplets(container)
            rmakers.trivialize(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_rest_filled(command_target)
            command_target = abjad.select.tuplets(container)
            rmakers.rewrite_sustained(command_target)
            rmakers.extract_trivial(container)  # ?
        if rewrite is not None:
            meter_command = RewriteMeterCommand(boundary_depth=rewrite)
            nested_music = abjad.mutate.eject_contents(container)
            metered_staff = rmakers.wrap_in_time_signature_staff(
                container[:], time_signatures
            )
            meter_command(metered_staff)
            music = abjad.mutate.eject_contents(metered_staff)
        else:
            music = abjad.mutate.eject_contents(container)

        return music

    return returned_function


def zero_padding_glissando(selections):
    for run in abjad.select.runs(selections):
        leaves = abjad.select.leaves(run)
        for leaf in leaves[1:-1]:
            if abjad.get.has_indicator(leaf, abjad.Tie):
                abjad.detach(abjad.Tie(), leaf)
    abjad.glissando(selections[:], zero_padding=True, allow_repeats=True)
    for run in abjad.select.runs(selections):
        leaves = abjad.select.leaves(run)
        for leaf in leaves[1:-1]:
            if isinstance(leaf, abjad.Note):
                abjad.tweak(leaf.note_head, r"\tweak Accidental.stencil ##f")
                abjad.tweak(leaf.note_head, r"\tweak transparent ##t")
                abjad.tweak(leaf.note_head, r"\tweak X-extent #'(0 . 0)")
            elif isinstance(leaf, abjad.Chord):
                for head in leaf.note_heads:
                    abjad.override(leaf).Accidental.stencil = "##f"
                    abjad.override(leaf).NoteHead.transparent = "##t"
                    abjad.tweak(head, r"\tweak X-extent #'(0 . 0)")
                    abjad.override(leaf).NoteHead.X_extent = "#'(0 . 0)"


def upward_gliss(selections, zero_padding=True):
    ties = abjad.select.logical_ties(selections, pitched=True)
    groups = []
    sub_group = []
    for tie in ties:
        if len(sub_group) < 1:
            sub_group.append(tie)
        else:
            if tie[0].written_pitch < sub_group[-1][0].written_pitch:
                groups.append(sub_group)
                sub_group = [tie]
            else:
                sub_group.append(tie)
    if 1 < len(sub_group):
        groups.append(sub_group)
    for group in groups:
        leaves = abjad.select.leaves(group)
        if zero_padding is True:
            zero_padding_glissando(leaves)
        else:
            abjad.glissando(leaves, hide_middle_note_heads=True)


def downward_gliss(selections, zero_padding=True):
    ties = abjad.select.logical_ties(selections, pitched=True)
    groups = []
    sub_group = []
    for tie in ties:
        if len(sub_group) < 1:
            sub_group.append(tie)
        else:
            if sub_group[-1][0].written_pitch < tie[0].written_pitch:
                groups.append(sub_group)
                sub_group = [tie]
            else:
                sub_group.append(tie)
    if 1 < len(sub_group):
        groups.append(sub_group)
    for group in groups:
        leaves = abjad.select.leaves(group)
        if zero_padding is True:
            zero_padding_glissando(leaves)
        else:
            abjad.glissando(leaves, hide_middle_note_heads=True)


def swipe_stems(selections):
    literals = evans.CyclicList(
        [
            r"\swipeUpStemOn",
            r"\swipeDownStemOn",
        ],
        forget=False,
    )
    for leaf in abjad.select.leaves(selections, pitched=True):
        direction = literals(r=1)[0]
        literal = abjad.LilyPondLiteral(direction, site="before")
        abjad.attach(literal, leaf)

    last_leaf = abjad.select.leaf(selections, -1, pitched=True)
    abjad.attach(abjad.LilyPondLiteral(r"\stemOff", site="after"), last_leaf)


def boolean_vector_to_indices(vector=[True, False]):
    out = []
    for i, boolean_value in enumerate(vector):
        if boolean_value is True:
            out.append(i)
    return out


def ficta_accidentals(force_accidentals=True):  # from trinton
    def returned_function(score, force_accidentals=force_accidentals):
        pties = abjad.select.logical_ties(score, pitched=True)

        ficta_ties = []
        chords = []
        post_graces = []

        for tie in pties:
            previous_leaf = abjad.select.with_previous_leaf(tie)[0]
            tie_duration = abjad.get.duration(tie)
            previous_duration = abjad.get.duration(previous_leaf)
            if isinstance(tie[0], abjad.Chord):
                chords.append(tie)
            if previous_duration < abjad.Duration(1, 16):
                if isinstance(tie[0], abjad.Chord):
                    pass
                else:
                    ficta_ties.append(tie)
            previous_parentage = abjad.get.parentage(previous_leaf).parent
            if (
                isinstance(previous_parentage, abjad.BeforeGraceContainer)
                or isinstance(previous_parentage, abjad.OnBeatGraceContainer)
                or isinstance(previous_parentage, abjad.AfterGraceContainer)
            ):
                tie_parentage = abjad.get.parentage(tie[0]).parent
                if (
                    isinstance(tie_parentage, abjad.BeforeGraceContainer)
                    or isinstance(tie_parentage, abjad.OnBeatGraceContainer)
                    or isinstance(tie_parentage, abjad.AfterGraceContainer)
                ):
                    pass
                else:
                    post_graces.append(tie)

        for tie in post_graces:
            abjad.attach(
                abjad.LilyPondLiteral(
                    r"\revert Staff.Accidental.X-extent", site="before"
                ),
                tie[0],
            )
            abjad.attach(
                abjad.LilyPondLiteral(
                    r"\override Staff.Accidental.X-extent = ##f", site="absolute_after"
                ),
                tie[-1],
            )

        for chord in chords:
            abjad.attach(
                abjad.LilyPondLiteral(
                    r"\revert Staff.Accidental.X-extent", site="before"
                ),
                chord[0],
            )
            abjad.attach(
                abjad.LilyPondLiteral(
                    r"\override Staff.Accidental.X-extent = ##f", site="absolute_after"
                ),
                chord[-1],
            )

            if force_accidentals is True:
                for head in chord[0].note_heads:
                    head.is_forced = True

        ficta_ties = abjad.select.group_by_contiguity(ficta_ties)

        for group in ficta_ties:
            first_tie = group[0]
            last_tie = group[-1]

            abjad.attach(
                abjad.LilyPondLiteral(
                    r"\override Staff.Accidental.stencil = ##f", site="before"
                ),
                first_tie[0],
            )

            abjad.attach(
                abjad.LilyPondLiteral(
                    r"\revert Staff.Accidental.stencil", site="absolute_after"
                ),
                last_tie[-1],
            )

            for tie in group:
                previous_leaf = abjad.select.with_previous_leaf(tie)[0]
                if isinstance(previous_leaf, abjad.Rest):
                    previous_leaf_pitch = abjad.NamedPitch("c,,,,,,,,,,,,,,,,")
                else:
                    previous_leaf_pitch = previous_leaf.written_pitch
                first_leaf = tie[0]
                first_leaf_pitch = first_leaf.written_pitch
                accidental = first_leaf_pitch.accidental
                accidental_name = accidental.name
                clef = abjad.get.effective(first_leaf, abjad.Clef)

                # if clef.name == "percussion" or first_leaf_pitch == previous_leaf_pitch:
                if (
                    clef.name == "percussion"
                    or first_leaf_pitch.name == previous_leaf_pitch.name
                ):
                    pass

                else:
                    abjad.attach(
                        abjad.Articulation(f"{accidental_name}-articulation"),
                        first_leaf,
                    )

    return returned_function


def label_logical_ties(selections):
    ties = abjad.select.logical_ties(selections, pitched=True)
    for i, tie in enumerate(ties):
        abjad.attach(abjad.Markup(rf"\markup {i}"), tie[0], direction=abjad.UP)


def treat_tuplets(container):
    command_target = abjad.select.tuplets(container)
    rmakers.trivialize(command_target)
    command_target = abjad.select.tuplets(container)
    rmakers.rewrite_rest_filled(command_target)
    command_target = abjad.select.tuplets(container)
    rmakers.rewrite_sustained(command_target)
    rmakers.extract_trivial(container)


def treat_tuplets(selections, index):
    command_target = abjad.select.tuplets(selections)
    command_target = command_target[index]
    # print(command_target)
    rmakers.trivialize(command_target)
    command_target = abjad.select.tuplets(selections)
    command_target = command_target[index]
    rmakers.rewrite_rest_filled(command_target)
    command_target = abjad.select.tuplets(selections)
    command_target = command_target[index]
    rmakers.rewrite_sustained(command_target)
    command_target = abjad.select.tuplets(selections)
    command_target = command_target[index]
    rmakers.extract_trivial(command_target)


def toggle_tuplets(selections, index):
    command_target = abjad.select.tuplets(selections)
    command_target = command_target[index]
    # print(command_target)
    command_target.toggle_prolation()


def make_artificial_harmonic_chords(selections, intervals=None):
    def sounding_pitch(higher, lower):
        r"Returns the sounding pitch of the harmonic as an |abjad.Pitch|."
        interval = abs(higher - lower).semitones
        sounding_pitch_dict = {
            1: 48,
            2: 36,
            3: 31,
            4: 28,
            5: 24,
            7: 19,
            9: 28,
            12: 12,
            16: 28,
            19: 19,
            24: 24,
            28: 28,
        }
        try:
            sounding_pitch = (
                abjad.NumberedPitch(lower).number + sounding_pitch_dict[interval]
            )
        except:
            sounding_pitch = None
        # except KeyError as err:
        #     raise ValueError(
        #         "cannot calculate sounding pitch for given interval"
        #     ) from err
        return sounding_pitch

    cyc_intervals = CyclicList(intervals, forget=False)
    ties = abjad.select.logical_ties(selections, pitched=True)
    for tie in ties:
        if isinstance(tie[0], abjad.Note):
            if intervals is None:
                continue
            else:
                durations = [leaf.written_duration for leaf in tie]
                pitch = tie[0].written_pitch
                interval = abjad.NumberedInterval(cyc_intervals(r=1)[0])
                touch = interval.transpose(pitch)
                new_leaves = [
                    abjad.Chord([pitch, touch], duration) for duration in durations[1:]
                ]
                sound = sounding_pitch(touch, pitch)
                if sound is not None:
                    new_leaves = [
                        abjad.Chord([pitch, touch, sound], durations[0])
                    ] + new_leaves
                else:
                    new_leaves = [
                        abjad.Chord([pitch, touch], durations[0])
                    ] + new_leaves
                if 1 < len(new_leaves):
                    abjad.tie(new_leaves)
                new_tie = abjad.LogicalTie(new_leaves)
                abjad.annotate(new_tie[0], "artificial", True)
                abjad.mutate.replace(tie, new_tie)
        elif isinstance(tie[0], abjad.Chord):
            assert len(tie[0].written_pitches) < 3
            pitches = list(tie[0].written_pitches)
            if len(pitches) == 1:
                continue
            else:
                sound = sounding_pitch(pitches[1], pitches[0])
                if sound is not None:
                    new_head = abjad.NoteHead(sound)
                    tie[0].note_heads.append(new_head)
                    abjad.annotate(tie[0], "artificial", True)
        else:
            raise Exception(
                f"Object must be of type abjad.Note or abjad.Chord NOT {type(tie[0])}"
            )


def decorate_artificial_harmonic_chords(selections):
    ties = abjad.select.logical_ties(selections, pitched=True)
    for tie in ties:
        if abjad.get.annotation(tie[0], "artificial") is not None:
            for leaf in tie:
                abjad.tweak(leaf.note_heads[1], r"\tweak style #'harmonic")
            top = tie[0].note_heads[2]
            top.is_parenthesized = True
            abjad.tweak(top, r"\tweak font-size #-4")
            abjad.tweak(top, r"\tweak Accidental.font-size #-4")
            abjad.tweak(top, r"\tweak Dots.font-size #-4")


def add_bowings(full_bow=False, stop_on_string=False):
    def returned_function(selections):
        if full_bow is True:
            cyc_bowings = CyclicList(
                ["baca-full-downbow", "baca-full-upbow"], forget=False
            )
        elif stop_on_string is True:
            cyc_bowings = CyclicList(
                ["baca-stop-on-string-full-downbow", "baca-stop-on-string-full-upbow"],
                forget=False,
            )
        else:
            cyc_bowings = CyclicList(["downbow", "upbow"], forget=False)
        ties = abjad.select.logical_ties(selections, pitched=True)
        first_heads = [_[0] for _ in ties]
        for head in first_heads:
            abjad.attach(abjad.Articulation(cyc_bowings(r=1)[0]), head)

    return returned_function


cutaway_commands = [
    abjad.LilyPondLiteral(r"\stopStaff", site="before"),
    abjad.LilyPondLiteral(
        r"\override Staff.StaffSymbol.transparent = ##f", site="before"
    ),
    abjad.LilyPondLiteral(r"\override Staff.Rest.transparent = ##f", site="before"),
    abjad.LilyPondLiteral(r"\override Staff.Dots.transparent = ##f", site="before"),
    abjad.LilyPondLiteral(r"\startStaff", site="before"),
    Attachment(
        abjad.LilyPondLiteral(r"\stopStaff", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    Attachment(
        abjad.LilyPondLiteral(
            r"\override Staff.StaffSymbol.transparent = ##t", site="after"
        ),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    Attachment(
        abjad.LilyPondLiteral(r"\override Staff.Rest.transparent = ##t", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    Attachment(
        abjad.LilyPondLiteral(r"\override Staff.Dots.transparent = ##t", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
    Attachment(
        abjad.LilyPondLiteral(r"\startStaff", site="after"),
        selector=lambda _: abjad.select.leaf(_, -1),
    ),
]


def bracket_time_duration(selections):
    leaves = abjad.select.leaves(selections)
    counts = [_ for _ in range(len(leaves))]
    effective_tempi = [abjad.get.effective(_, abjad.MetronomeMark) for _ in leaves]

    def get_effective(list, i):
        if list[i] is not None:
            return list[i]
        else:
            return get_effective(list, i - 1)

    def result(component, list, i):
        return (
            component._get_duration()
            / get_effective(list, i).reference_duration
            / get_effective(list, i).units_per_minute
            * 60
        )

    calculated_durations = [
        result(leaf, effective_tempi, i) for leaf, i in zip(leaves, counts)
    ]
    total_duration = float(sum(calculated_durations))
    # raise Exception(total_duration)
    def format_seconds(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}'{seconds:02}''"

    formatted_time_string = format_seconds(total_duration)
    abjad.attach(
        abjad.LilyPondLiteral(
            rf'\timeBracket "{formatted_time_string}" {{ ', site="before"
        ),
        leaves[0],
    )
    abjad.attach(
        abjad.LilyPondLiteral("}", site="after"),
        leaves[-1],
    )


def staff_changes(reservoir, sequence):

    derived_sequence = CyclicList([reservoir[_] for _ in sequence], forget=False)

    def returned_function(selections):
        ties = abjad.select.logical_ties(selections)
        for tie in ties:
            location = derived_sequence(r=1)[0]
            literal = abjad.LilyPondLiteral(
                rf'\once \change Staff = "{location}"', site="before"
            )
            abjad.attach(literal, tie[0])

    return returned_function


def gliss_only(selections, hide_stems=False, hide_flags=False):
    for run in abjad.select.runs(selections):
        leaves = abjad.select.leaves(run)
        for leaf in leaves:
            if abjad.get.has_indicator(leaf, abjad.Tie):
                abjad.detach(abjad.Tie(), leaf)
    abjad.glissando(selections[:], zero_padding=True, allow_repeats=True)
    for run in abjad.select.runs(selections):
        leaves = abjad.select.leaves(run)
        for leaf in leaves:
            if isinstance(leaf, abjad.Note):
                abjad.tweak(leaf.note_head, r"\tweak Accidental.stencil ##f")
                abjad.tweak(leaf.note_head, r"\tweak transparent ##t")
                abjad.tweak(leaf.note_head, r"\tweak X-extent #'(0 . 0)")
            elif isinstance(leaf, abjad.Chord):
                for head in leaf.note_heads:
                    abjad.override(leaf).Accidental.stencil = "##f"
                    abjad.override(leaf).NoteHead.transparent = "##t"
                    abjad.tweak(head, r"\tweak X-extent #'(0 . 0)")
                    abjad.override(leaf).NoteHead.X_extent = "#'(0 . 0)"
        if hide_stems is True:
            abjad.attach(
                abjad.LilyPondLiteral(
                    [
                        r"\override Staff.Stem.stencil = ##f",
                    ],
                    site="before",
                ),
                run[0],
            )
            abjad.attach(
                abjad.LilyPondLiteral(
                    [
                        r"\override Staff.Stem.stencil = ##t",
                    ],
                    site="after",
                ),
                run[-1],
            )
        if hide_flags is True:
            abjad.attach(
                abjad.LilyPondLiteral(
                    [r"\override  Staff.Flag.stencil = ##f"], site="before"
                ),
                run[0],
            )
            abjad.attach(
                abjad.LilyPondLiteral(
                    [r"\override  Staff.Flag.stencil = ##t"], site="after"
                ),
                run[-1],
            )


def change_duration_log(selections, value=2, pitched=True):
    for leaf in abjad.select.leaves(selections, pitched=pitched):
        abjad.override(leaf).note_head.duration_log = value
