\version "2.19.82"

\paper {}

    \score {
      \new Staff


c'4
^\markup {
        \scale
            #'(0.4 . 0.4)
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
                            \override NoteHead.transparent = ##t
                            \override Beam.padding = #0
                            tupletFullLength = ##t
                        }
                        {
                            \slashedGrace {
                            \override Beam.grow-direction = #LEFT
                            \featherDurations #(ly:make-moment 4/3)
                            {
                            c'32^\markup{\tiny \halign #-1.6 "jeté"}
                            [
                            c'32
                            c'32
                            c'32
                            c'32
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
            }
}
