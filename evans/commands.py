import abjad


class Command(object):
    def __init__(
        self, command=None, contents=None, indicator=None, selector=None, voice_name=None,
    ):
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

        >>> score = abjad.Score([abjad.Staff("c'4 c'4 c'4 c'4", name="staff one")])
        >>> command = evans.Command(
        ...     command="attach",
        ...     indicator=abjad.Markup("*", direction="up"),
        ...     selector=abjad.select().leaves(pitched=True).get([1])[0],
        ...     voice="staff one"
        ... )
        ...
        >>> command(score)
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
        voice = score[self.voice_name]
        if self.command == "attach":
            abjad.attach(self.indicator, self.selector(voice))
        elif self.command == "detach":
            abjad.detach(self.indicator, self.selector(voice))
        elif self.command == "replace":
            self._replace(voice, self.contents, self.selector)
        else:
            raise Exception(f"Invalid command {self.command}")

    def _replace(self, voice, contents, selector):
        target = selector(voice)
        for tuplet in abjad.select(target).tuplets():
            maker = abjad.LeafMaker()
            abjad.mutate(tuplet).replace(maker([0], [abjad.inspect(tuplet).duration()]))
        target = selector(voice)
        abjad.mutate(abjad.select(target).leaves()).replace(contents[:])


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


class HandlerCommand(object):
    def __init__(self, voice_name, timespan, handler):
        self.voice_name = voice_name
        self.timespan = timespan
        self.handler = handler

class RhythmCommand(object):
    def __init__(self, voice_name, timespan, handler):
        self.voice_name = voice_name
        self.timespan = timespan
        self.handler = handler
