\version "2.23.14" % temp
%%% JETE MARKUP %%%


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
    \postscript "
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

%%% BOWSTROKE MARKUP %%%

baca-full-downbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.downbow"
    \path #0.15
    #'(
        (moveto 0.7375 0.05)
        (rlineto 1 0)
        (closepath)
        )

baca-full-upbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.upbow"
    \path #0.15
    #'(
        (moveto 0.62 2.005)
        (rlineto 1 0)
        (closepath)
        )

baca-stop-on-string-markup =
    \markup
    \path #0.15
    #'(
        (moveto 0 0)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

baca-stop-on-string-full-downbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.downbow"
    \path #0.15
    #'(
        (moveto 0.7375 0.05)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

baca-stop-on-string-full-upbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.upbow"
    \path #0.15
    #'(
        (moveto 0.62 2.005)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

%{ \concat {
\translate #'(0.2 . 0.75)
\scale #'(0.4 . 0.4) \concat {\translate #'(0 . 0) 45 \translate #'(0 . 1) \teeny o}
} %}


evans-counterclockwise-arc = \markup {
    \translate #'(0 . 1.5)
    \postscript "
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


%%% rehearsal mark %%%

rehearsal-mark-markup = #(
    define-music-function
    (string font-size h-align)
    (string? number? number?)
    #{
    - \tweak font-size #font-size
    - \markup
    \with-dimensions-from \null
    \halign #h-align
    \override #'(box-padding . 0.5)
    \override #'(font-name . "Bell MT")
    \box
    { \combine \halign #0 #string \halign #0 \transparent "O" }
    #}
    )

%%% boxed markups %%%

boxed-markup = #(
    define-music-function
    (string font-size)
    (string? number?)
    #{
    - \tweak font-size #font-size
    ^ \markup
    \override #'(style . "box")
    \override #'(box-padding . 0.5)
    \whiteout
    \box
    \italic
    #string
    #}
    )

boxed-markup-down = #(
    define-music-function
    (string font-size)
    (string? number?)
    #{
    - \tweak font-size #font-size
    _ \markup
    \override #'(style . "box")
    \override #'(box-padding . 0.5)
    \whiteout
    \box
    \italic
    #string
    #}
    )

%%% ekmelos markups %%%

normal-pressure = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xe11b
}

half-pressure = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xf67d
}

full-pressure = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xe11a
}

diamond-notehead-markup = \markup \musicglyph "noteheads.s0harmonic"
default-notehead-markup = \markup \musicglyph "noteheads.s1"
half-diamond-notehead-markup = \markup {
    \fontsize #5
    \override #'(font-name . "ekmelos")
    \char ##xe0fc
}

quarter-pedal = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xf6ba
}

half-pedal = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xf6bb
}

three-quarter-pedal = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xf6bc
}

full-pedal = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xf6bd
}

%%% chop bowings %%%

down-bow-towards-body-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee80
}

up-bow-towards-body-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee81
}

down-bow-away-from-body-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee82
}

up-bow-away-from-body-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee83
}

down-bow-beyond-bridge-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee84
}

up-bow-beyond-bridge-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee85
}

scrape-parallel-inward-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee86
}

scrape-parallel-outward-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee87
}

scrape-circular-clockwise-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee88
}

scrape-circular-counterclockwise-markup = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xee89
}

smorz-text = \markup "smorz."

square-element = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xeab8
}

loop-element = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xeac3
}

wiggle-element = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xeaf2
}

random-element = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xeaf0
}

random-element-two = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xeaf1
}

random-element-three = \markup {
    \fontsize #1
    \override #'(font-name . "ekmelos")
    \char ##xeaf2
}


#(define-markup-command
    (flute-heel-rotation-markup layout props number)
    (number?)
    (interpret-markup layout props
    #{
    \markup \rotate #number \musicglyph "scripts.upedalheel"
    #}))

tongue-t = \markup \rotate #0 \override #'(font-size . -3) \override #'(font-family . sans) "T"

tongue-t-inverted = \markup \rotate #-180 \override #'(font-size . -3) \override #'(font-family . sans) "T"

tongue-t-circled = \markup \override #'(thickness . 2.5) \circle \rotate #0 \override #'(font-size . -3) \override #'(font-family . sans) "T"

air-tone-markup = \markup {
    \fontsize #6.5
    \override #'(font-name . "ekmelos")
    \char ##xe114
}
half-air-tone-markup = \markup {
    \fontsize #6.5
    \override #'(font-name . "ekmelos")
    \char ##xe115
}

key-click-plus-markup = \markup "+"

trem-one-markup = \markup {
    \fontsize #6.5
    \override #'(font-name . "ekmelos")
    \char ##xe220
}

trem-two-markup = \markup {
    \fontsize #6.5
    \override #'(font-name . "ekmelos")
    \char ##xe221
}

trem-three-markup = \markup {
    \fontsize #6.5
    \override #'(font-name . "ekmelos")
    \char ##xe222
}

trem-four-markup = \markup {
    \fontsize #6.5
    \override #'(font-name . "ekmelos")
    \char ##xe223
}

trem-five-markup = \markup {
    \fontsize #6.5
    \override #'(font-name . "ekmelos")
    \char ##xe224
}
