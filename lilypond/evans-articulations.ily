#(ly:set-option 'relative-includes #t)
\include "evans-markups.ily"

%%% LEAVE FILE-FINAL: %%%

\layout {
    \context {
        \Score
        scriptDefinitions = #default-script-alist
    }
}
