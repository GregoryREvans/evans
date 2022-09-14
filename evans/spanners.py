import dataclasses

import abjad


class DurationLine:  # don't forget to force notehead shape

    ### CLASS VARIABLES ###

    __slots__ = "_tweaks"

    _site = "after"

    _time_orientation = abjad.enums.RIGHT

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        tweaks=None,
    ):
        if tweaks is not None:  # WARNING: tweakinterface removed
            assert isinstance(tweaks, abjad.TweakInterface), repr(tweaks)
        self._tweaks = abjad.TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return f"<{type(self).__name__}()>"

    def __str__(self):
        return r"\-"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def tweaks(self):
        return self._tweaks


class Lyrics(
    abjad.Context
):  # save lyrics to variable in lib.ily like -> var = \lyricsto "context" { LYRICS }

    ### CLASS VARIABLES ###

    __documentation_section__ = "Contexts"

    __slots__ = ()

    _default_lilypond_type = "Lyrics"

    ### INITIALIZER ###

    # TODO: make keywords mandatory
    def __init__(  # see: https://lilypond.org/doc/v2.23/Documentation/notation/common-notation-for-vocal-music
        self,
        components=None,
        lilypond_type: str = "Lyrics",
        lyrics: str = r"\lyrics",
        simultaneous: bool = False,
        name: str = None,
        tag: abjad.Tag = None,
        *,
        language: str = "english",
    ) -> None:
        abjad.Context.__init__(
            self,
            components=components,
            language=language,
            lilypond_type=lilypond_type,
            simultaneous=simultaneous,
            name=name,
            tag=tag,
        )
        lyrics_literal = abjad.LilyPondLiteral(f"{lyrics}")
        abjad.attach(lyrics_literal, self)

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self):
        return super().tag


class BendBefore:

    _site = "before"
    _is_dataclass = True
    _time_orientation = abjad.RIGHT

    def __init__(
        self,
        bend_amount=-4,
        tweaks=None,
    ):
        self.bend_amount = bend_amount
        self.tweaks = tweaks

    # TODO: remove
    def __str__(self) -> str:
        if self.bend_amount < 0:
            out_string = f"""#(ly:expect-warning "Unattached BendAfterEvent")\n\\bendBeforeNegative #'{self.bend_amount}"""
        else:
            out_string = f"""#(ly:expect-warning "Unattached BendAfterEvent")\n\\bendBeforePositive #'{self.bend_amount}"""
        return out_string

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle
