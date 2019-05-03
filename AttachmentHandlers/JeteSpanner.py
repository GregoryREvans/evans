import abjad

class JeteSpanner:

    # def __init__(
    #     self,
    #     pitch_list=None,
    #     continuous=True,
    #     ):
    #     def cyc(lst):
    #         if self.continuous == False:
    #             self._count = 0
    #         while True:
    #             yield lst[self._count % len(lst)]
    #             self._count += 1
    #     self.pitch_list = pitch_list
    #     self.continuous = continuous
    #     self._cyc_pitches = cyc(pitch_list)
    #     self._count = 0

    def __call__(self, selections):
        return self._apply_jete(selections)

    def _apply_jete(self, selections):
        container = abjad.Container()
        container.append(selections)
        span_literal = r'''- \abjad-solid-line-with-hook
- \tweak bound-details.left.text'''
        jete_string = r'''scale #'(0.45 . 0.45)
        \score
            {
                \new Score
                \with
                {
                    \override SpacingSpanner.spacing-increment = #0.5
                    proportionalNotationDuration = ##f
                }
                <<
                    \new RhythmicStaff
                    \with
                    {
                        \remove Time_signature_engraver
                        \remove Staff_symbol_engraver
                        \override Stem.direction = #up
                        \override Stem.length = #5
                        \override TupletBracket.bracket-visibility = ##t
                        \override TupletBracket.direction = #up
                        \override TupletBracket.minimum-length = #4
                        \override TupletBracket.padding = #1.25
                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                        \override TupletNumber.font-size = #-3
                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                        \override Dots.stencil = ##f
                        tupletFullLength = ##t
                    }
                    {
                    \grace {
                                \override Beam.grow-direction = #LEFT
                                \featherDurations #(ly:make-moment 4/3)
                                {
                                    \tweak transparent ##t
                                    c'32 ^\markup{\fontsize #2 \halign #-1.2 "gett."}
                                    [
                                    \tweak transparent ##t
                                    c'32
                                    \tweak transparent ##t
                                    c'32
                                    \tweak transparent ##t
                                    c'32
                                    \tweak transparent ##t
                                    c'32
                                    \tweak transparent ##t
                                    c'32
                                    ]
                                }
                           }
                    }
                >>
                \layout {
                            indent = #0
                            ragged-right = ##t
                        }
            }
                    '''
        mark = abjad.Markup(direction=abjad.Up)
        mark = mark.with_literal(jete_string)
        tweak_text = r'''- \tweak bound-details.right.padding 3'''
        final_starter = abjad.LilyPondLiteral(f'{span_literal} {mark} {tweak_text} \startTextSpan', format_slot="after")
        stop_indicator = abjad.LilyPondLiteral(r'''\stopTextSpan''', format_slot='after')
        for run in abjad.select(container).runs():
            if len(run) > 1:
                abjad.attach(final_starter, run[0])
                abjad.attach(stop_indicator, abjad.inspect(run[-1]).leaf(1))
            else:
                abjad.attach(mark, run[0])

        return container[:]

###DEMO###
contents = [abjad.Note(), abjad.Rest()]
staff = abjad.Staff()
for item in contents:
    staff.append(item)
jete_span = JeteSpanner()
jete_span(staff)
abjad.show(staff)
