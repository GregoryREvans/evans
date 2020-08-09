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
    ):
        self.callable = callable
        self.command = command
        self.contents = contents
        self.indicator = indicator
        self.selector = selector
        self.voice_name = voice_name

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
            ...     indicator=abjad.Markup("*", direction="up"),
            ...     selector=abjad.select().leaves(pitched=True).get([1])[0],
            ...     voice_name="staff one"
            ... )
            ...
            >>> command(score)
            >>> abjad.show(score) # doctest: +SKIP

            .. docs::

                >>> print(abjad.lilypond(score))
                \new Score
                <<
                    \context Staff = "staff one"
                    {
                        c'4
                        c'4
                        ^ \markup { * }
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
        else:
            raise Exception(f"Invalid command {self.command}")

    def _replace(self, voice, contents, selection):
        abjad.mutate(selection[:]).replace(contents[:])


def attach(voice_name, indicator, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
    return Command(
        command="attach", indicator=indicator, selector=selector, voice_name=voice_name,
    )


def detach(voice_name, indicator, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
    return Command(
        command="detach", indicator=indicator, selector=selector, voice_name=voice_name,
    )


def replace(voice_name, contents, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
    return Command(
        command="replace", contents=contents, selector=selector, voice_name=voice_name,
    )


def call(voice_name, callable, selector=None):
    if selector is None:
        selector = abjad.select().leaf(0)
    return Command(
        command="call", callable=callable, selector=selector, voice_name=voice_name,
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


class RhythmCommand:
    def __init__(self, voice_name, timespan, handler):
        self.voice_name = voice_name
        self.timespan = timespan
        self.handler = handler

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)
