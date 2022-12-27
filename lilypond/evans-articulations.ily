\version "2.23.14" % temp
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


#(append! default-script-alist
 (list
  `("downbowtowardsbody"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,down-bow-towards-body-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

down-bow-towards-body = #(make-articulation 'downbowtowardsbody)


#(append! default-script-alist
 (list
  `("upbowtowardsbody"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,up-bow-towards-body-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

up-bow-towards-body = #(make-articulation 'upbowtowardsbody)


#(append! default-script-alist
 (list
  `("downbowawayfrombody"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,down-bow-away-from-body-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

down-bow-away-from-body = #(make-articulation 'downbowawayfrombody)


#(append! default-script-alist
 (list
  `("upbowawayfrombody"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,up-bow-away-from-body-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

up-bow-away-from-body = #(make-articulation 'upbowawayfrombody)


#(append! default-script-alist
 (list
  `("downbowbeyondbridge"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,down-bow-beyond-bridge-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

down-bow-beyond-bridge = #(make-articulation 'downbowbeyondbridge)


#(append! default-script-alist
 (list
  `("upbowbeyondbridge"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,up-bow-beyond-bridge-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

up-bow-beyond-bridge = #(make-articulation 'upbowbeyondbridge)


#(append! default-script-alist
 (list
  `("scrapeparallelinward"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,scrape-parallel-inward-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

scrape-parallel-inward = #(make-articulation 'scrapeparallelinward)


#(append! default-script-alist
 (list
  `("scrapeparalleloutward"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,scrape-parallel-outward-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

scrape-parallel-outward = #(make-articulation 'scrapeparalleloutward)


#(append! default-script-alist
 (list
  `("scrapecircularclockwise"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,scrape-circular-clockwise-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

scrape-circular-clockwise = #(make-articulation 'scrapecircularclockwise)


#(append! default-script-alist
 (list
  `("scrapecircularcounterclockwise"
     . (
         (stencil . ,ly:text-interface::print)
         (text . ,scrape-circular-counterclockwise-markup)
         (avoid-slur . around)
         (direction . ,UP)
         (padding . 0.20)
         (script-priority . 150)
         (skyline-horizontal-padding . 0.20)
         (toward-stem-shift . 0.5)
         ))))

scrape-circular-counterclockwise = #(make-articulation 'scrapecircularcounterclockwise)



%%% LEAVE FILE-FINAL: %%%

\layout {
    \context {
        \Score
        scriptDefinitions = #default-script-alist
    }
}
