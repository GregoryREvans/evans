%%% JETE MARKUP %%%

ferneyhough-gettato-markup =
\markup {
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
                        \override NoteHead.transparent = ##t
                        \override Beam.padding = #0
                        tupletFullLength = ##t
                    }
                    {
                        \slashedGrace {
                        \override Beam.grow-direction = #LEFT
                        \featherDurations #(ly:make-moment 4/3)
                        {
                        c'32^\markup{\large \halign #-1.3 "gett."}
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


piston-jete-markup =
\markup {
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
                        \override Stem.stencil = ##f
                        \override Stem.direction = #down
                        \override Slur.thickness = #4
                        \override Dots.stencil = ##f
                        \override Flag.stencil = ##f
                        \override NoteHead.font-size = #-4
                        \override NoteHead.transparent = ##t
                    }
                    {
                        c'32.^\markup{\large \halign #-1.3 "jeté"}
                        \staccato
                        (
                        c'32.
                        \staccato
                        c'32.
                        \staccato
                        c'32.
                        \staccato
                        )
                    }
                >>
                \layout {
                    indent = #0
                    ragged-right = ##t
                }
            }
        }

evans-upbow = #"scripts.upbow"

evans-downbow = #"scripts.downbow"

evans-vspace = \vspace #0.20
