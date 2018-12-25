import abjad

class GlissandoHandler:

    def __init__(
        self,
        glissando_style=None,
        line_style=None,
        ):
        self.glissando_style = glissando_style
        self.line_style = line_style

    def __call__(self, selections):
        return self.add_glissando(selections)

    def add_glissando(self, selections):
        runs = abjad.select(selections).runs()
        if self.glissando_style == 'hide_middle_note_heads':
            if self.line_style == 'jete':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('dotted-line').style, hide_middle_note_heads=True, )
            elif self.line_style == 'trill':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('trill').style, hide_middle_note_heads=True, )
            elif self.line_style == 'zigzag':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('zigzag').style, hide_middle_note_heads=True, )
            elif self.line_style == 'dashed':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('dashed-line').style, hide_middle_note_heads=True, )
            else:
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], hide_middle_note_heads=True, )
        elif self.glissando_style == 'hide_middle_stems':
            if self.line_style == 'jete':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('dotted-line').style, hide_middle_note_heads=True, hide_middle_stems=True, )
            elif self.line_style == 'trill':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('trill').style, hide_middle_note_heads=True, hide_middle_stems=True, )
            elif self.line_style == 'zigzag':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('zigzag').style, hide_middle_note_heads=True, hide_middle_stems=True, )
            elif self.line_style == 'dashed':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('dashed-line').style, hide_middle_note_heads=True, hide_middle_stems=True, )
            else:
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], hide_middle_note_heads=True, hide_middle_stems=True, )
        else:
            if self.line_style == 'jete':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('dotted-line').style, allow_repeats=True, allow_ties=True, parenthesize_repeats=True, )
            elif self.line_style == 'trill':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('trill').style, allow_repeats=True, allow_ties=True, parenthesize_repeats=True, )
            elif self.line_style == 'zigzag':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('zigzag').style, allow_repeats=True, allow_ties=True, parenthesize_repeats=True, )
            elif self.line_style == 'dashed':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], abjad.tweak('dashed-line').style, allow_repeats=True, allow_ties=True, parenthesize_repeats=True, )
            else:
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], allow_repeats=True, allow_ties=True, parenthesize_repeats=True,)
        return selections
