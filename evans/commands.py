"""
Command classes.
"""
import abjad


class Command:
    def __init__(
        self,
        callable=None,
        command=None,
        contents=None,
        indicator=None,
        selector=None,
        voice_name=None,
        source_voice_name=None,
        target_voice_name=None,
    ):
        self.callable = callable
        self.command = command
        self.contents = contents
        self.indicator = indicator
        self.selector = selector
        self.voice_name = voice_name
        self.source_voice_name = source_voice_name
        self.target_voice_name = target_voice_name

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)

    def __call__(self, score):
        r"""
        Calls command on Score.

        .. container:: example

            >>> score = abjad.Score([abjad.Staff("c'4 c'4 c'4 c'4", name="staff one")])
            >>> command = evans.Command(
            ...     command="attach",
            ...     indicator=abjad.Markup(r"\markup *", direction="up"),
            ...     selector=abjad.select().leaves(pitched=True).get([1])[0],
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
            ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
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
            abjad.attach(self.indicator, selection)
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


def attach(voice_name, indicator, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
    return Command(
        command="attach",
        indicator=indicator,
        selector=selector,
        voice_name=voice_name,
    )


def detach(voice_name, indicator, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
    return Command(
        command="detach",
        indicator=indicator,
        selector=selector,
        voice_name=voice_name,
    )


def replace(voice_name, contents, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
    return Command(
        command="replace",
        contents=contents,
        selector=selector,
        voice_name=voice_name,
    )


def call(voice_name, callable, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
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
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)


class Attachment:
    def __init__(
        self,
        indicator,
        selector=None,
    ):
        self.indicator = indicator
        self.selector = selector


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
            abjad.select().leaf(0, pitched=True),
        ),
        evans.attachment(
            abjad.Markup(r"\evans-custom-markup", direction=abjad.Up),
            abjad.select().leaf(0, pitched=True),
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
                            run_ties = (
                                abjad.select(selections)
                                .runs()
                                .logical_ties(pitched=True)
                            )
                            ties_first_leaves = abjad.Selection(
                                [_[0] for _ in run_ties]
                            )
                            return ties_first_leaves

                    else:
                        selector = abjad.select().leaf(0, pitched=True)
                    new_attachment = Attachment(
                        arg,
                        selector,
                    )
                    self.attachments.append(new_attachment)
                elif callable(arg):
                    new_callable = Callable(
                        arg,
                        abjad.select().leaves(),
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
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)


class RhythmCommand:
    def __init__(self, voice_name, timespan, handler):
        self.voice_name = voice_name
        self.timespan = timespan
        self.handler = handler

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)


class Skeleton:
    def __init__(self, string):
        self.selections = self.skeleton(string)

    def __call__(self, durations):
        if abjad.get.duration(self.selections) == abjad.Duration(sum(durations)):
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
        elif isinstance(argument, abjad.Selection):
            selection = argument
        else:
            message = "evans.skeleton() accepts string or selection,"
            message += " not {repr(argument)}."
            raise TypeError(message)
        return selection
