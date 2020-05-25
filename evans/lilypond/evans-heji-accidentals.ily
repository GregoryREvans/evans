%%%install ekmelos in lilypond itself
%%%read pdf for character associations.

%%% tempered natural %%%
tempered-natural =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2f2
            }
        $note #})

%%% tempered sharp %%%
tempered-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2f3
            }
        $note #})

%%% tempered flat %%%
tempered-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2f1
            }
        $note #})


%%% natural comma down %%%
nat-comma-down =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2c2
            }
        $note #})

%%% septimal comma down %%%
septimal-comma-down =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \concat {
                    \fontsize #4
                    \override #'(font-name . "ekmelos")
                    \char ##xe2de
                    \musicglyph #"accidentals.flat"
                }
            }
        $note #})

%%% undecimal quarter sharp %%%
undecimal-quarter-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2e3
            }
        $note #})

%%% tridecimal third flat %%%
tridecimal-third-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2e4
            }
        $note #})

%%% 17 schisma up %%%
seventeen-schisma-up =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2e7
            }
        $note #})

%%% 19 schisma down %%%
nineteen-schisma-down =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2e8
            }
        $note #})

%%% mixed %%%
mixed-test =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \concat {
                    \fontsize #4
                    \override #'(font-name . "ekmelos")
                    \char ##xe2e7
                    \musicglyph #"accidentals.sharp"
                }
            }
        $note #})

%%% flat 17 up %%%
flat-up =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \concat {
                    \fontsize #4
                    \override #'(font-name . "ekmelos")
                    \char ##xe2e6
                    \fontsize #4
                    \override #'(font-name . "ekmelos")
                    \char ##xe2c6
                }
            }
        $note #})

%%% sharp 19 down %%%
sharp-down =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \concat {
                    \fontsize #4
                    \override #'(font-name . "ekmelos")
                    \char ##xe2e9
                    \musicglyph #"accidentals.flat"
                }
            }
        $note #})
