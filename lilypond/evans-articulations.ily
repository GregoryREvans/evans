\include "evans-markups.ily"
%%% JETE ARTICULATIONS %%%

#(append! default-script-alist
   (list
    `("ferneyhoughgettato"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,ferneyhough-gettato-markup)
           (avoid-slur . around)
           (direction . ,UP)
           (self-alignment-X . ,LEFT)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.5)
           ))))

ferneyhough-gettato = #(make-articulation "ferneyhoughgettato")



#(append! default-script-alist
   (list
    `("pistonjete"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,piston-jete-markup)
           (avoid-slur . around)
           (direction . ,UP)
           (self-alignment-X . ,LEFT)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.5)
           (left-padding . 1)
           ))))

piston-jete = #(make-articulation "pistonjete")


%%% LEAVE FILE-FINAL: %%%

\layout {
    \context {
        \Score
        scriptDefinitions = #default-script-alist
    }
}
