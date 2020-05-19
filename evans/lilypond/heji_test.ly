\version "2.19.84"  %! abjad.LilyPondFile._get_format_pieces()
\language "english" %! abjad.LilyPondFile._get_format_pieces()
\include "evans-heji-accidentals.ily"


\layout{\accidentalStyle dodecaphonic}
\paper {#(include-special-characters)}

\score {
    \new Staff
    {
            \tempered-natural
            c'16

            \nat-comma-down
            e'16

            g'16

            \septimal-comma-down
            bf'16

			d'16

            \undecimal-quarter-sharp
            f'16

            \tridecimal-third-flat
            a'16

            \flat-up
            cs''32

            \sharp-down
            ef''32
    }
}
