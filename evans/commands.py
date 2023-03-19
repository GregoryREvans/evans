"""
Command classes.
"""
import abjad
import baca
# import dataclasses
# import typing
import quicktions
from abjadext import rmakers

from .handlers import IntermittentVoiceHandler, RhythmHandler
from .rtm import RTMMaker, exponential_leaf_maker
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


def talea(
    counts,
    denominator,
    *,
    end_counts=(),
    extra_counts=(),
    preamble=(),
    previous_state=None,
    read_talea_once_only=False,
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


def make_tied_notes(preprocessor=None, rewrite=False, treat_tuplets=True):
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
    rewrite=None,
    treat_tuplets=True,
):

    maker = RhythmHandler(RTMMaker(rtm), forget=False)

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
    hocket=False,
    truncate_ties=False,
):
    def _find_parent(selections):
        first_leaf = abjad.select.leaf(selections, 0)
        parentage = abjad.get.parentage(first_leaf)
        parent_voice = abjad.select.components(parentage, abjad.Voice)
        return f"{parent_voice[0].name} temp"

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

    imbrications = baca.imbricate(
        original_voice,
        "v1",
        pitches,
        allow_unused_pitches=allow_unused_pitches,
        by_pitch_class=by_pitch_class,
        hocket=hocket,
        truncate_ties=truncate_ties,
    )
    imbrication = imbrications["v1"][0]
    contents = abjad.mutate.eject_contents(imbrication)
    intermittent_voice.extend(contents)

    groups = rmakers.nongrace_leaves_in_each_tuplet(intermittent_voice)
    rmakers.beam_groups(groups, beam_rests=True)
    if articulation is not None:
        for head in baca.select.pheads(intermittent_voice):
            abjad.attach(abjad.Articulation(articulation), head)
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
