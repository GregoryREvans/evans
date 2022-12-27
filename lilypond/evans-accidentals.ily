\version "2.23.14"
\language "english"
\include "evans-accidentals-markups.ily"


one-quarter-flat-black = {
    \tweak Accidental.stencil #ly:text-interface::print
    \tweak Accidental.text \one-quarter-flat-markup-black
}

one-quarter-flat-thin = {
    \tweak Accidental.stencil #ly:text-interface::print
    \tweak Accidental.text \one-quarter-flat-markup-thin
}

three-quarter-flat-black = {
    \tweak Accidental.stencil #ly:text-interface::print
    \tweak Accidental.text \three-quarters-flat-markup-black
}

three-quarter-flat-thin = {
    \tweak Accidental.stencil #ly:text-interface::print
    \tweak Accidental.text \three-quarters-flat-markup-thin
}

one-quarter-sharp-short = {
    \tweak Accidental.stencil #ly:text-interface::print
    \tweak Accidental.text \one-quarter-sharp-markup-short
}

one-quarter-sharp-tall = {
    \tweak Accidental.stencil #ly:text-interface::print
    \tweak Accidental.text \one-quarter-sharp-markup-tall
}

three-quarters-sharp-big = {
    \tweak Accidental.stencil #ly:text-interface::print
    \tweak Accidental.text \three-quarters-sharp-markup
}
