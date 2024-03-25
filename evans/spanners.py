# import dataclasses

import abjad

from .select import get_top_level_components_from_leaves
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


def make_multi_trill(
    note,
    *trill_pitches,
    notehead_styles=[None],
    after_spacing="1/16",
    extra_padding=0,
    with_notes=False,
):
    """
    sample pitches:
    c'!
    cqs''!
    <d'! fqs'!>
    !! requires evans.ily and abjad.ily
    """
    if isinstance(note, abjad.LogicalTie):
        tie = note
        note = note[0]
    else:
        tie = abjad.select.logical_ties(note)
    _notehead_styles = []
    for _ in notehead_styles:
        if _ is not None:
            _notehead_styles.append(_)
        else:
            _notehead_styles.append("")
    heads = CyclicList(_notehead_styles, forget=False)
    t_length = len(trill_pitches)
    assert 0 < t_length < 5
    opening_literal = abjad.LilyPondLiteral(
        rf"\afterGrace {after_spacing}", site="before"
    )
    abjad.attach(opening_literal, note)
    if t_length == 1:
        closing_literal = abjad.LilyPondLiteral(
            [
                "{",
                rf"   {heads(r=1)[0]} \suggest-pitch-middle \parentheAll {trill_pitches[0]}32 \startTrillSpan",
                # used to end with \revert-noteheads
                "}",
            ],
            site="after",
        )
        abjad.attach(closing_literal, note)
        stop_trill = abjad.LilyPondLiteral(r"\stopTrillSpan", site="after")
        if with_notes is False:
            final_tie_leaf = tie[-1]
        elif with_notes is True:
            final_tie_leaf = note
        next = abjad.get.leaf(final_tie_leaf, 1)
        abjad.attach(stop_trill, next)
    if t_length == 2:
        closing_literal = abjad.LilyPondLiteral(
            [
                "{",
                rf"""     \suggest-pitch-open {heads(r=1)[0]} {trill_pitches[0]}32 \startDoubleTrill #{2 + extra_padding} #{1 + extra_padding} """,
                rf"""     \suggest-pitch-close {heads(r=1)[0]} {trill_pitches[1]}32""",
                # used to end with \revert-noteheads
                "}",
            ],
            site="after",
        )
        abjad.attach(closing_literal, note)
        stop_trill = abjad.LilyPondLiteral(r"\stopDoubleTrill", site="after")
        if with_notes is False:
            final_tie_leaf = tie[-1]
        elif with_notes is True:
            final_tie_leaf = note
        next = abjad.get.leaf(final_tie_leaf, 1)
        abjad.attach(stop_trill, next)
    if t_length == 3:
        closing_literal = abjad.LilyPondLiteral(
            [
                "{",
                rf"""     \suggest-pitch-open {heads(r=1)[0]} {trill_pitches[0]}32 \startTripleTrill #{3 + extra_padding} #{2 + extra_padding} #{1 + extra_padding} """
                rf"     \suggest-pitch-middle {heads(r=1)[0]} {trill_pitches[1]}32"
                rf"""     \suggest-pitch-close {heads(r=1)[0]} {trill_pitches[2]}32"""
                # used to end with \revert-noteheads
                "}",
            ],
            site="after",
        )
        abjad.attach(closing_literal, note)
        stop_trill = abjad.LilyPondLiteral(r"\stopTripleTrill", site="after")
        if with_notes is False:
            final_tie_leaf = tie[-1]
        elif with_notes is True:
            final_tie_leaf = note
        next = abjad.get.leaf(final_tie_leaf, 1)
        abjad.attach(stop_trill, next)


def annotate_tuplet_duration(
    selections, exclude_durations=[(1, 4)], paddings=[2.5], directions=["#up"]
):
    paddings = CyclicList(paddings, forget=False)
    directions = CyclicList(directions, forget=False)
    exclude_durations = [abjad.Duration(_) for _ in exclude_durations]
    leaves = abjad.select.leaves(selections)
    top_level_components = get_top_level_components_from_leaves(leaves)
    tuplets = abjad.select.tuplets(top_level_components)
    for tuplet in tuplets:
        parent = abjad.get.parentage(tuplet).parent
        if isinstance(parent, abjad.Tuplet):
            continue
        tup_dur = abjad.get.duration(tuplet)
        if tup_dur in exclude_durations:
            continue
        group_start = abjad.StartGroup()
        group_stop = abjad.StopGroup()
        notes = abjad.makers.make_leaves([0], [tup_dur])
        string = abjad.illustrators.selection_to_score_markup_string(notes)
        string = rf"""\markup {{ \hspace #1.25 "(" \hspace #-0.5 \scale #'(0.5 . 0.5) {string} \hspace #-0.5 ")" }}"""
        direction = directions(r=1)[0]
        padding = paddings(r=1)[0]
        bundle = abjad.Bundle(
            indicator=group_start,
            tweaks=(
                abjad.Tweak(rf"- \tweak HorizontalBracket.direction {direction}"),
                abjad.Tweak(r"- \tweak HorizontalBracket.transparent ##t"),
                abjad.Tweak(rf"- \tweak HorizontalBracket.padding {padding}"),
                abjad.Tweak(r"- \tweak HorizontalBracketText.Y-offset -0.5"),
                abjad.Tweak(rf"- \tweak HorizontalBracketText.text {string}"),
            ),
        )
        # abjad.override(group_start).HorizontalBracket.transparent = True
        # abjad.override(group_start).padding = 2.5
        # abjad.override(group_start).HorizontalBracketText.Y_offset = -0.5
        # abjad.override(group_start).HorizontalBracketText.text = string
        first_leaf = abjad.select.leaf(tuplet, 0)
        last_leaf = abjad.select.leaf(tuplet, -1)
        abjad.attach(bundle, first_leaf)
        abjad.attach(group_stop, last_leaf)
