"""
Command classes.
"""
# import dataclasses
# import typing

import abjad
import baca
from abjadext import rmakers

from .handlers import RhythmHandler


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
            voice = score[self.voice_name]
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
    forget=False,
    preprocessor=None,
    rewrite_meter=None,
):
    commands = []
    arguments = []
    for arg in args:
        if issubclass(arg.__class__, rmakers.Command):
            commands.append(arg)
        else:
            arguments.append(arg)
    if rewrite_meter is not None:
        stack = rmakers.stack(
            rmaker,
            *commands,
            rmakers.trivialize(lambda _: abjad.select.tuplets(_)),
            rmakers.rewrite_rest_filled(lambda _: abjad.select.tuplets(_)),
            rmakers.rewrite_sustained(lambda _: abjad.select.tuplets(_)),
            rmakers.extract_trivial(),
            rmakers.RewriteMeterCommand(
                boundary_depth=rewrite_meter,
                reference_meters=[
                    abjad.Meter((4, 4))
                ],  # reference meters is for constructing special offset inventories (i.e. akasha 6/8)
            ),
            preprocessor=preprocessor,
        )
        handler = RhythmHandler(
            stack,
            forget=forget,
        )
    else:
        stack = rmakers.stack(
            rmaker,
            *commands,
            rmakers.trivialize(lambda _: abjad.select.tuplets(_)),
            rmakers.rewrite_rest_filled(lambda _: abjad.select.tuplets(_)),
            rmakers.rewrite_sustained(lambda _: abjad.select.tuplets(_)),
            rmakers.extract_trivial(),
            preprocessor=preprocessor,
        )
        handler = RhythmHandler(
            stack,
            forget=forget,
        )

    out = MusicCommand(
        location,
        handler,
        *arguments,
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


def hairpin(dynamics, *tweaks, selector):
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
):
    def returned_function(divisions, state=state, previous_state=previous_state):
        music = rmakers.accelerando(
            divisions,
            interpolations,
            previous_state=previous_state,
            spelling=spelling,
            state=state,
            tag=tag,
        )
        return music

    return returned_function


def even_division(
    denominators,
    denominator="from_counts",
    *,
    extra_counts=(0,),
    previous_state=None,
    spelling=rmakers.Spelling(
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        increase_monotonic=False,
    ),
    state=None,
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=state, previous_state=previous_state):
        music = rmakers.even_division(
            divisions,
            denominators=denominators,
            extra_counts=extra_counts,
            previous_state=previous_state,
            spelling=spelling,
            state=state,
            tag=tag,
        )
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
    spelling=rmakers.Spelling(
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        increase_monotonic=False,
    ),
    state=None,
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=state, previous_state=previous_state):
        music = rmakers.talea(
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
        return music

    return returned_function


def tuplet(
    tuplet_ratios,
    *,
    denominator=None,
    spelling=rmakers.Spelling(
        forbidden_note_duration=None,
        forbidden_rest_duration=None,
        increase_monotonic=False,
    ),
    tag=abjad.Tag(string=""),
):
    def returned_function(divisions, state=None, previous_state=None):
        music = rmakers.tuplet(
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
        return music

    return returned_function
