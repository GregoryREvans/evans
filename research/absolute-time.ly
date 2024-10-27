\version "2.23.81"
\language "english"
#(set-default-paper-size "letterportrait")
#(set-global-staff-size 12) % 20 is standard part size

%{ \paper {
  page-breaking = #ly:one-line-auto-height-breaking
} %}

\header {
	tagline = ##f
	breakbefore = ##t
	title =  \markup \center-column {
            \override #'(font-name . "Bell MT")
            \fontsize #14
            \line {
                \concat {
                P
                \hspace #1
                O
                \hspace #1
                L
                \hspace #1
                I
                \hspace #1
                L
                \hspace #1
                L
                \hspace #1
				A
                \hspace #1
				S
                \hspace #1
                }
            }
    }
	composer = \markup \override #'(font-name . "Bell MT") \fontsize #3 {"Gregory Rowland Evans (*1995)"}
	tagline = \markup { "" }
}


\layout {
  \context {
    \Score
    proportionalNotationDuration = #(ly:make-moment 1/15)
    \override SpacingSpanner.uniform-stretching = ##t
    %{ \override DurationLine.bound-details.right.end-style = #'hook %}
    \override DurationLine.thickness = 2.5
  }
  \context {
    \Voice
    \consists Duration_line_engraver
    \remove Stem_engraver
    \remove Dots_engraver
    \override NoteHead.duration-log = 2
  }
}

at =
#(define-music-function (instrument point pitch len) (string? exact-rational? ly:pitch? exact-rational?)
   #{ \context Staff = #instrument \new Voice \after 4*#point { $pitch 4*#len \- } <> #})

\markup \center-column {
       \override #'(font-name . "Bell MT")
       \fontsize #7
       \line {
           \concat {
           M
           \hspace #1
           O
           \hspace #1
           V
           \hspace #1
           E
           \hspace #1
           M
           \hspace #1
           E
           \hspace #1
           N
           \hspace #1
           T
           \hspace #2
           1
           }
       }
}
\score {
    \new Score
        <<
          \new Staff = piano { s1*10 }
          \new Staff = violin { s1*10 }
          \cadenzaOn
          \at piano ##e0.5 e' ##e1.0
          \at piano ##e0.75 fs' ##e1.0
          \at piano ##e1.0 g' ##e4
          \at piano ##e2.5 cs' ##e0.5

          \at violin ##e0.6 e' ##e1.5
          \at violin ##e3.0 c'' ##e1.125
        >>
}

\markup \center-column {
       \override #'(font-name . "Bell MT")
       \fontsize #7
       \line {
           \concat {
           M
           \hspace #1
           O
           \hspace #1
           V
           \hspace #1
           E
           \hspace #1
           M
           \hspace #1
           E
           \hspace #1
           N
           \hspace #1
           T
           \hspace #2
           1
           }
       }
}
\score {
    \new Score
        <<
          \new Staff = piano { s1*10 }
          \new Staff = violin { s1*10 }
          \cadenzaOn
          \at piano ##e0.5 e' ##e1.0
          \at piano ##e0.75 fs' ##e1.0
          \at piano ##e1.0 g' ##e4
          \at piano ##e2.5 cs' ##e0.5

          \at violin ##e0.6 e' ##e1.5
          \at violin ##e3.0 c'' ##e2.125
        >>
}
