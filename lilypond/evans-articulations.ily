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

%%%%


#(define evans-script-alist
  (cons*
      `(keyclickplus
         . (
            (script-stencil . (feta . ("stopped" . "stopped")))
            (side-relative-direction . ,DOWN)
            (quantize-position . #t)
            (avoid-slur . inside)
            (toward-stem-shift . 1.0)
            (toward-stem-shift-in-column . 0.0)
            (padding . 0.20)
            (skyline-horizontal-padding . 0.10)
            (script-priority . -100))
             )
      `(downbowtowardsbody
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,down-bow-towards-body-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(upbowtowardsbody
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,up-bow-towards-body-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(downbowawayfrombody
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,down-bow-away-from-body-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(upbowawayfrombody
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,up-bow-away-from-body-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(downbowbeyondbridge
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,down-bow-beyond-bridge-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(upbowbeyondbridge
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,up-bow-beyond-bridge-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(scrapeparallelinward
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,scrape-parallel-inward-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(scrapeparalleloutward
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,scrape-parallel-outward-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(scrapecircularclockwise
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,scrape-circular-clockwise-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
      `(scrapecircularcounterclockwise
         . (
             (stencil . ,ly:text-interface::print)
             (text . ,scrape-circular-counterclockwise-markup)
             (avoid-slur . around)
             (direction . ,UP)
             (padding . 0.20)
             (script-priority . 150)
             (skyline-horizontal-padding . 0.20)
             (toward-stem-shift . 0.5)
             ))
             `(bacafulldownbow
               . (
                 (stencil . ,ly:text-interface::print)
                 (text . ,baca-full-downbow-markup)
                 (avoid-slur . around)
                 (direction . ,UP)
                 (padding . 0.20)
                 (script-priority . 150)
                 (skyline-horizontal-padding . 0.20)
                 (toward-stem-shift . 0.5)
                 ))
             `(bacastoponstringfulldownbow
               . (
                 (stencil . ,ly:text-interface::print)
                 (text . ,baca-stop-on-string-full-downbow-markup)
                 (avoid-slur . around)
                 (direction . ,UP)
                 (padding . 0.20)
                 (script-priority . 150)
                 (skyline-horizontal-padding . 0.20)
                 (toward-stem-shift . 0.6)
                 ))
             `(bacafullupbow
               . (
                 (stencil . ,ly:text-interface::print)
                 (text . ,baca-full-upbow-markup)
                 (avoid-slur . around)
                 (direction . ,UP)
                 (padding . 0.20)
                 (script-priority . 150)
                 (skyline-horizontal-padding . 0.20)
                 (toward-stem-shift . 0.5)
                 ))
             `(bacastoponstringfullupbow
               . (
                 (stencil . ,ly:text-interface::print)
                 (text . ,baca-stop-on-string-full-upbow-markup)
                 (avoid-slur . around)
                 (direction . ,UP)
                 (padding . 0.20)
                 (script-priority . 150)
                 (skyline-horizontal-padding . 0.20)
                 (toward-stem-shift . 0.6)
                 ))
             `(bacastoponstring
               . (
                 (stencil . ,ly:text-interface::print)
                 (text . ,baca-stop-on-string-markup)
                 (avoid-slur . around)
                 (padding . 0.20)
                 (script-priority . 150)
                 (side-relative-direction . ,DOWN)
                 (skyline-horizontal-padding . 0.20)
                 (toward-stem-shift . 0.4)
                 ))
  default-script-alist))

  key-click-plus = #(make-articulation 'keyclickplus)



baca-full-downbow = #(make-articulation 'bacafulldownbow)

baca-stop-on-string-full-downbow = #(
    make-articulation 'bacastoponstringfulldownbow)

baca-full-upbow = #(make-articulation 'bacafullupbow)

baca-stop-on-string-full-upbow = #(
    make-articulation 'bacastoponstringfullupbow)

baca-stop-on-string = #(make-articulation 'bacastoponstring)

  down-bow-towards-body = #(make-articulation 'downbowtowardsbody)
  up-bow-towards-body = #(make-articulation 'upbowtowardsbody)
  down-bow-away-from-body = #(make-articulation 'downbowawayfrombody)
  up-bow-away-from-body = #(make-articulation 'upbowawayfrombody)
  down-bow-beyond-bridge = #(make-articulation 'downbowbeyondbridge)
  up-bow-beyond-bridge = #(make-articulation 'upbowbeyondbridge)
  scrape-parallel-inward = #(make-articulation 'scrapeparallelinward)
  scrape-parallel-outward = #(make-articulation 'scrapeparalleloutward)
  scrape-circular-clockwise = #(make-articulation 'scrapecircularclockwise)
  scrape-circular-counterclockwise = #(make-articulation 'scrapecircularcounterclockwise)

%%% LEAVE FILE-FINAL: %%%

\layout {
    \context {
        \Score
        scriptDefinitions = #evans-script-alist
    }
}
