from fractions import Fraction

import abjad

from .sequence import CyclicList


class Breaks:
    def __init__(
        self,
        *pages,
        bar_number=0,
        default_spacing=(1, 24),
        spacing=None,
        time_signatures=None,
        # if it's just a segment and not the score, add header_block = abjad.Block(name="header") header_block.items.append(r"composer = ##f poet = ##f title = ##f")
        # tell segment maker to behave differently if we use breaks
    ):
        systems = []
        self.pages = []
        for page in pages:
            self.pages.append(page)
            for system in page.systems:
                systems.append(system)
        self._page_break_indices = abjad.Sequence(
            [_.total_measures for _ in self.pages]
        )
        self.page_break_indices = abjad.math.cumulative_sums(self._page_break_indices)[
            1:
        ]
        self._system_break_indices = abjad.Sequence(
            [_.system_break_indices for _ in self.pages]
        ).flatten()
        self.system_break_indices = abjad.math.cumulative_sums(
            self._system_break_indices.items
        )[1:]
        self.bar_number = bar_number
        self.default_spacing = default_spacing
        self.lbsd = CyclicList([_.lbsd for _ in systems], forget=False)
        if spacing is not None:
            self.spacing = CyclicList(spacing, forget=False)
            self.spacing_indices = [_[0] - 1 for _ in spacing]
        else:
            self.spacing = []
            self.spacing_indices = []
        self.time_signatures = time_signatures
        self.x_offsets = CyclicList([_.x_offset for _ in systems], forget=False)

    def make_score(self):
        score = abjad.Score(name="Score")
        abjad.setting(score).currentBarNumber = self.bar_number
        global_context = abjad.Staff(
            name="Global Context", lilypond_type="TimeSignatureContext"
        )
        layout_context = abjad.Staff(name="Layout", lilypond_type="LayoutContext")
        for time_signature in self.time_signatures:
            multiplier = abjad.Multiplier(time_signature.pair)
            skip = abjad.Skip((1, 1), multiplier=multiplier)
            layout_context.append(skip)
        global_context.append(layout_context)
        score.append(global_context)
        return score

    def make_document_layout(self, path):
        score = self.make_score()
        leaves = abjad.Selection(score).leaves()
        no_breaks_literal = abjad.LilyPondLiteral(
            r"\autoPageBreaksOff", format_slot="before"
        )
        abjad.attach(no_breaks_literal, leaves[0])
        lbsd_values = self.lbsd(r=1)[0]
        lbsd_literal = abjad.LilyPondLiteral(
            fr"\evans-lbsd #{lbsd_values[0]} #'{lbsd_values[1]}", format_slot="before"
        )
        abjad.attach(lbsd_literal, leaves[0])
        x_offset = self.x_offsets(r=1)[0]
        x_offset_literal = abjad.LilyPondLiteral(
            fr"\evans-system-X-offset #{x_offset}", format_slot="before"
        )
        abjad.attach(x_offset_literal, leaves[0])
        for i, leaf in enumerate(leaves):
            # literal = abjad.LilyPondLiteral(r"\noBreak", format_slot="before")
            # abjad.attach(literal, leaf)
            test_case = i + 1
            if i in self.spacing_indices:
                space = self.spacing(r=1)[0][1]
                spacing_string = fr"\evans-new-spacing-section #{space[0]} #{space[1]}"
                spacing_literal = abjad.LilyPondLiteral(
                    spacing_string, format_slot="before"
                )
                abjad.attach(spacing_literal, leaf)
            else:
                if test_case in self.system_break_indices:
                    default_frac = Fraction(
                        self.default_spacing[0], self.default_spacing[1]
                    )
                    multiplier = Fraction(35, 24)
                    new_frac = default_frac * multiplier
                    spacing_string = fr"\evans-new-spacing-section #{new_frac.numerator} #{new_frac.denominator}"
                else:
                    spacing_string = fr"\evans-new-spacing-section #{self.default_spacing[0]} #{self.default_spacing[1]}"
                spacing_literal = abjad.LilyPondLiteral(
                    spacing_string, format_slot="before"
                )
                abjad.attach(spacing_literal, leaf)
        for page_break_index in self.page_break_indices:
            relevant_leaf = leaves[page_break_index - 1]
            literal = abjad.LilyPondLiteral(r"\pageBreak", format_slot="after")
            abjad.attach(literal, relevant_leaf)
        for system_break_index in self.system_break_indices:
            relevant_leaf = leaves[system_break_index - 1]
            literal = abjad.LilyPondLiteral(r"\break", format_slot="after")
            abjad.attach(literal, relevant_leaf)
            lbsd_values = self.lbsd(r=1)[0]
            lbsd_literal = abjad.LilyPondLiteral(
                fr"\evans-lbsd #{lbsd_values[0]} #'{lbsd_values[1]}",
                format_slot="after",
            )
            abjad.attach(lbsd_literal, relevant_leaf)
            x_offset = self.x_offsets(r=1)[0]
            x_offset_literal = abjad.LilyPondLiteral(
                fr"\evans-system-X-offset #{x_offset}", format_slot="after"
            )
            abjad.attach(x_offset_literal, relevant_leaf)
        for leaf in leaves:
            if not abjad.get.has_indicator(
                leaf, abjad.LilyPondLiteral(r"\break", format_slot="after")
            ):
                no_break = abjad.LilyPondLiteral(r"\noBreak", format_slot="after")
                abjad.attach(no_break, leaf)
        with open(f"{path}/layout.ly", "w") as fp:
            s = abjad.lilypond(score)
            fp.writelines(s)


class Page:
    def __init__(
        self,
        *systems,
    ):
        self.total_measures = 0
        self.systems = []
        for system in systems:
            self.systems.append(system)
            self.total_measures += system.measures
        self.system_break_indices = []
        if 1 < len(self.systems):
            for system in self.systems:
                self.system_break_indices.append(system.measures)


class System:
    def __init__(
        self,
        lbsd=None,
        measures=None,
        x_offset=0,
    ):
        self.lbsd = lbsd
        self.measures = measures
        self.x_offset = x_offset


def reduce_fermata_measures(time_signatures, fermata_measures):
    new_time_signatures = [_ for _ in time_signatures[:-1]]
    for fermata_index in fermata_measures:
        new_time_signatures[fermata_index] = abjad.TimeSignature((1, 4))
    return new_time_signatures


def join_time_signature_lists(nested_time_sigatures):
    out = []
    for time_signature_list in nested_time_sigatures:
        out.extend(time_signature_list)
    return out
