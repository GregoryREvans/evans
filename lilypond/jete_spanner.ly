\version "2.19.82"

\paper {}

\markup\vspace #.5
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%here starts the snippet:

strokeUp = \markup\combine\override #'(thickness . 1.3) \draw-line #'(0 . 2.8)\raise #2.8 \arrow-head #Y #UP ##f
strokeDown = \markup\combine\arrow-head #Y #DOWN ##f \override #'(thickness . 1.3) \draw-line #'(0 . 2.8)

RHp = \rightHandFinger #1
RHi = \rightHandFinger #2
RHm = \rightHandFinger #3
RHa = \rightHandFinger #4
RHx = \rightHandFinger #5
RHu = \rightHandFinger \strokeUp
RHd = \rightHandFinger \strokeDown

rasgUp = {
  \once\override TextSpanner.style = #'line
  \once\override TextSpanner.thickness = #1.3
  \once\override TextSpanner.bound-details.left.padding = #-0.5
  \once\override TextSpanner.bound-details.left.text =
    \markup {
  \general-align #Y #DOWN {
    \epsfile #X #6 #"jete.eps"
  }
}
  \override TextSpanner.bound-details.right.text =
    \markup\concat {
      \hspace # -.4 \magnify #0.7
      \column {
        \override #'(thickness . 1.3)
        \draw-line #'(0.2 . -0.2)
      }
    }
  \once\override TextSpanner.bound-details.right.padding = #-0.5
}

rasgDown = {
  \once\override TextSpanner.style = #'line
  \once\override TextSpanner.thickness = #1.3
  \once\override TextSpanner.bound-details.left.padding = #-0.5
  \once\override TextSpanner.bound-details.left.text =
    \markup\concat {
      \magnify #0.7 \fontsize #2 \raise #1.1 \rotate # 90
      \concat {
        \musicglyph #"scripts.trill_element"
        \musicglyph #"scripts.trill_element"
        \musicglyph #"scripts.trill_element"
      }
      \hspace # -0.2
    }
  \override TextSpanner.bound-details.right.text =
    \markup\concat {
      \hspace # -.4 \magnify #0.7
      \column {
        \fontsize #2
        \override #'(thickness . 1.3)
        \draw-line #'(0 . -2.8)
        \vspace # -.2
        \fontsize #2
        \arrow-head #Y #DOWN ##f
      }
    }
  \once\override TextSpanner.bound-details.right.padding = #-0.5
}

musicOne = {
  \set strokeFingerOrientations = #'(up)
  \override StrokeFinger.add-stem-support = ##t
  \override StrokeFinger.staff-padding = #5
  \override NoteColumn.ignore-collision = ##t
  \partial 4
  <a, e a cis' e'>8
  - \tweak bound-details.left.text \markup {
                    \scale
                        #'(0.75 . 0.75)
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
                                        \override Staff.fontSize = #-8
                                        tupletFullLength = ##t
                                    }
                                    {
                                        \slashedGrace {
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 1
                                        c'128
                                        [
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        c'64
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        c'32
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        c'16
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 0
                                        c'8
                                        ]
                                    }
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                        }
\startTextSpan
  <a, e a cis' e'>8
  <e, b, e gis d' e'\RHd>4
  \tuplet 3/2 { \rasgUp <e, b, e gis d' e'>8 \startTextSpan q q }
  q4 \stopTextSpan
  <e, b, e gis d' e'\RHd>8 <e, b, e gis d' e'\RHu>
  s8
}

fingOne = {
  \set strokeFingerOrientations = #'(down)
  \stemUp
  \hideNotes
  \partial 4 s4
  s4 e,8*2/3\RHa e,\RHm e,\RHi e,4\RHi e,8\RHi e,\RHi
}

\markup\italic\concat { "Right hand movment ends up (tanguillo)"\hspace #.3 ":" }

\score {
  \new Staff <<
    \clef "G_8"
    \key a\major
    \context Voice = "Soprano" { \voiceOne << \musicOne >> }
    \context Voice = "Alto" { \voiceTwo << \fingOne >> }
  >>
  \layout { }
}

musicTwo = {
  \set strokeFingerOrientations = #'(up)
  \override StrokeFinger.add-stem-support = ##t
  \override NoteColumn.ignore-collision = ##t
  \partial 4
  <e, b, e gis b e'\RHd>8  <e, b, e gis b e'\RHu>
  \rasgDown <f a c' e'>16 \startTextSpan q q  \stopTextSpan
    <f a c' e'\RHu> <f a c' e'\RHd>8 <f a c' e'\RHu>
    \rasgDown <e, b, e gis b e'>16 \startTextSpan q q  \stopTextSpan
    <e, b, e gis b e'\RHu>
  s8
}

fingTwo = {
  \set strokeFingerOrientations = #'(down)
  \stemUp
  \hideNotes
  \partial 4 s4
  e16\RHa e\RHm e\RHi e\RHi s4 e,16\RHa e,\RHm e,\RHi e,\RHi
}

\markup\italic\concat { "Right hand movment ends down (soléares)"\hspace #.3 ":" }

\score {
  \new Staff <<
    \clef "G_8"
    \time 3/4
    \context Voice = "Soprano" { \voiceOne << \musicTwo >> }
    \context Voice = "Alto" { \voiceTwo << \fingTwo >> }
  >>
  \layout { }
}
