%%%install HEJI in liypond itself
%%%read pdf for character associations.
%%% HEJI test %%%
heji-test =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\override #'(font-name . "HEJI") a}
        $note #})
