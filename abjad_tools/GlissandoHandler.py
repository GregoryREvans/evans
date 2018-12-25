import abjad

class GlissandoHandler:

    def __init__(
        self,
        glissando_style=None,
        line_style=None,
        ):
        self.glissando_style = glisando_style
        self.line_style = line_style

    def __call__(self, selections):
        return self.add_glissando(selections)

    def add_glissando(self, selections):
        runs = abjad.select(selections).runs()
        if self.glissando_style == 'stems':
            if self.line_style == 'jete':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], stems=True, style='dotted-line',)
            elif self.line_style == 'trill':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], stems=True, style='trill',)
            elif self.line_style == 'zigzag':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], stems=True, style='zigzag',)
            elif self.line_style == 'dashed':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], stems=True, style='dashed-line',)
            else:
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], stems=True, )
        else:
            if self.line_style == 'jete':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], allow_repeats=True, allow_ties=True, parenthesize_repeats=True, style='dotted-line',)
            elif self.line_style == 'trill':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], allow_repeats=True, allow_ties=True, parenthesize_repeats=True, style='trill',)
            elif self.line_style == 'zigzag':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], allow_repeats=True, allow_ties=True, parenthesize_repeats=True, style='zigzag',)
            elif self.line_style == 'dashed':
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], allow_repeats=True, allow_ties=True, parenthesize_repeats=True, style='dashed-line',)
            else:
                for run in runs:
                    if len(run) > 1:
                        abjad.glissando(run[:], allow_repeats=True, allow_ties=True, parenthesize_repeats=True,)
        return selections
