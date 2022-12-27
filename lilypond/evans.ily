\version "2.23.81" % temp
\include "evans-articulations.ily"
\include "evans-beam.ily"
\include "evans-clef.ily"
\include "evans-coloring.ily"
\include "evans-functions.ily"
\include "evans-grace-notes.ily"
\include "evans-grobs.ily"
\include "evans-markups.ily"
\include "evans-page-layout.ily"
\include "evans-spanners.ily"

\layout { % this is to beautify whiteout in grace notes
    \context {
        \Staff
        \override LedgerLineSpanner.layer = #3
    }
}
