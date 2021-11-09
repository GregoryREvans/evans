#(ly:set-option 'relative-includes #t)
\include "evans-markups.ily"

tongue =
#(define-music-function (parser location dots) (integer?)
  #{
    \tweak stencil
      #(lambda (grob)
        (let ((stil (ly:script-interface::print grob)))
          (let loop ((count (1- dots)) (new-stil stil))
            (if (> count 0)
                (loop (1- count)
                      (ly:stencil-combine-at-edge new-stil X RIGHT stil 0.2))
                (ly:stencil-aligned-to new-stil X CENTER)))))
     \staccato
  #})

%%% LEAVE FILE-FINAL: %%%

\layout {
    \context {
        \Score
        scriptDefinitions = #default-script-alist
    }
}
