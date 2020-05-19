\version "2.19.84"  %! abjad.LilyPondFile._get_format_pieces()
\language "english" %! abjad.LilyPondFile._get_format_pieces()
\include "evans-heji-accidentals.ily"


\layout{\accidentalStyle dodecaphonic}
\paper {#(include-special-characters)}

\score {
    \new Staff
    {
            \tempered-natural
            c'8

            \nat-comma-down
            e'8

            g'8

            \septimal-comma-down
            bf'8

            \undecimal-quarter-sharp
            f'8

            \tridecimal-third-flat
            a'8

            \seventeen-schisma-up
            cs''8

            \nineteen-schisma-down
            ef''8
    }
}
