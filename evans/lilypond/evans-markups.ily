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

evans-clockwise-arc = \markup {
    \translate #'(0 . 1.5)
    \postscript #"
        0 -0.5 0.5 90 -90 arc
        stroke
        gsave 0.1 setlinewidth
        -0.20 0.20 moveto
        0.13 -0.05 lineto
        -0.20 -0.30 lineto
        closepath
        fill
        stroke grestore
        "
}

%{ \concat {
\translate #'(0.2 . 0.75)
\scale #'(0.4 . 0.4) \concat {\translate #'(0 . 0) 45 \translate #'(0 . 1) \teeny o}
} %}


evans-counterclockwise-arc = \markup {
    \translate #'(0 . 1.5)
    \postscript #"
        0 -0.5 0.5 90 -90 arc
        stroke
        gsave 0.1 setlinewidth
        -0.20 -0.7 moveto
        0.13 -0.95 lineto
        -0.20 -1.2 lineto
        closepath
        fill
        stroke grestore
        "
}

%{ \concat {
\translate #'(0 . 0.75)
\scale #'(0.4 . 0.4) \concat {\translate #'(0 . 0.3) - \translate #'(0 . 0) 45 \translate #'(0 . 1) \teeny o}
} %}
