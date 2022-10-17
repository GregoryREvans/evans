# import dataclasses

import abjad
from .sequence import CyclicList

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


def make_fancy_gliss(*args, right_padding=0.5, match=True):
    if match is True:
        temp = []
        for arg in args:
            temp.append(arg)
            temp.append(arg * -1)
        args = temp
    lines = [
        r"\fancy-gliss",
        "   #'(",
    ]
    for i, arg in enumerate(args):
        s = f"      ({i} 0 {i}.5 {arg} {i + 1} 0)"
        lines.append(s)
    lines.append(f" )")
    lines.append(f" #{right_padding}")
    literal = abjad.LilyPondLiteral(lines, site="before")
    return literal


def make_multi_trill(note, *trill_pitches, notehead_styles=[r"\revert-noteheads"], after_spacing="1/16"):
    heads = CyclicList(notehead_styles, forget=False)
    t_length = len(trill_pitches)
    assert 0 < t_length < 5
    opening_literal = abjad.LilyPondLiteral(fr"\afterGrace {after_spacing}", site="after")
    abjad.attach(opening_literal, note)
    if t_length == 1:
        closing_literal = abjad.LilyPondLiteral(
            [
                "{",
                fr"   {heads(r=1)[0]} \parentheAll \suggest-pitch-middle {trill_pitches[0]}'!32 \startTrillSpan \revert-noteheads",
                "}"
            ],
            site="after"
        )
        abjad.attach(closing_literal, note)
        stop_trill = abjad.LilyPondLiteral(r"\stopTrillSpan", site="after")
        next = abjad.get.leaf(note, 1)
        abjad.attach(stop_trill, next)
    if t_length == 2:
        closing_literal = abjad.LilyPondLiteral(
            [
                "{",
                fr"""     \suggest-pitch-open {heads(r=1)[0]} {trill_pitches[0]}!32 \startDoubleTrill #2 #1 -\markup "(" """,
                fr"""     \suggest-pitch-close {heads(r=1)[0]} {trill_pitches[1]}!32 -\markup ")" """,
                "}",
            ],
            site="after"
        )
        abjad.attach(closing_literal, note)
        stop_trill = abjad.LilyPondLiteral(r"\stopDoubleTrill", site="after")
        next = abjad.get.leaf(note, 1)
        abjad.attach(stop_trill, next)
    if t_length == 3:
        closing_literal = abjad.LilyPondLiteral(
            [
                "{",
        			fr"""     \suggest-pitch-open {heads(r=1)[0]} {trill_pitches[0]}!32 \startTripleTrill #3 #2 #1 -\markup "(" """
        			fr"     \suggest-pitch-middle {heads(r=1)[0]} {trill_pitches[1]}!32"
        			fr"""     \suggest-pitch-close {heads(r=1)[0]} {trill_pitches[2]}!32 -\markup ")" """
                "}"
            ],
            site="after"
        )
        abjad.attach(closing_literal, note)
        stop_trill = abjad.LilyPondLiteral(r"\stopTripleTrill", site="after")
        next = abjad.get.leaf(note, 1)
        abjad.attach(stop_trill, next)
