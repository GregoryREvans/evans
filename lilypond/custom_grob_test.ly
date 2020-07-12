\version "2.19.84"
\language "english"


arrow-sharp = \markup {\musicglyph #"accidentals.sharp"
\postscript #"gsave 0.17 setlinewidth -0.91 1.25 moveto -0.91 2 lineto
stroke grestore
gsave 0.1 setlinewidth -1.21 1.4 moveto -0.91 2.18 lineto -0.61 1.4 lineto
stroke grestore"}

%test 1 works
%{ \layout {
  \context {
    \Score
    \override Accidental.stencil =
      #(lambda (grob)
         (let* (
                (glyph (ly:grob-property grob 'glyph-name))
                )
                 (cond
                  (
                     (equal? glyph "accidentals.sharp")
                     (grob-interpret-markup grob arrow-sharp)
                  )
                  (else (ly:accidental-interface::print grob))
                  )
         )
        )
  }
}

\new Score {
  \new Staff  {
    cf'
    c'
    cs'
    d'
    cs'
    c'
    cf'
    }
  } %}

%test 2 does not work correctly

accidentalGlyphs = #`(
    (,Sharp . "accidentals.sharp")
    (,Natural . "accidentals.natural")
    (,Flat . "accidentals.flat")
)

\layout {
  \context {
    \Score
    \override KeySignature.glyph-name-alist = \accidentalGlyphs
    \override Accidental.glyph-name-alist = \accidentalGlyphs
    \override AccidentalCautionary.glyph-name-alist = \accidentalGlyphs
    \override TrillPitchAccidental.glyph-name-alist = \accidentalGlyphs
    \override AmbitusAccidental.glyph-name-alist = \accidentalGlyphs
    \override Accidental.stencil =
      #(lambda (grob)
         (let* (
                (glyph (ly:grob-property grob 'glyph-name))
                )
                 (cond
                  (
                     (equal? glyph "accidentals.sharp")
                     (grob-interpret-markup grob arrow-sharp)
                  )
                  (else (ly:accidental-interface::print grob))
                  )
         )
        )
  }
}

\new Score {
  \new Staff  {
    cf'
    c'
    cs'
    d'
    cs'
    c'
    cf'
    }
  }
