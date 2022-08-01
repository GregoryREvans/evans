%! abjad.LilyPondFile._get_format_pieces()
\version "2.22.1"
%! abjad.LilyPondFile._get_format_pieces()
\language "english"
%! abjad.LilyPondFile._get_format_pieces()
\include "/Users/gregoryevans/evans/lilypond/evans-functions.ily"

\score
%! abjad.LilyPondFile._get_format_pieces()
{
    \new Score <<
        \new Staff {
            c'1 - \bendAfter #5
            e'1
            #(ly:expect-warning "Unattached BendAfterEvent")
            \bendBeforePositive #'5 d'1
            #(ly:expect-warning "Unattached BendAfterEvent")
            \bendBeforeNegative #'-5 e'
        }
    >>
}
