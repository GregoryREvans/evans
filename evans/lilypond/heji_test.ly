\version "2.19.84"  %! abjad.LilyPondFile._get_format_pieces()
\language "english" %! abjad.LilyPondFile._get_format_pieces()
\include "evans-heji-accidentals.ily"



\paper {#(include-special-characters)}

\score {
    \new Staff
    {
            \heji-numbers-test
            cs'1

            \heji-qwerty-test
            cs'1

            \heji-asdf-test
            cs'1

            \heji-zxc-test
            cs'1
    }
}
