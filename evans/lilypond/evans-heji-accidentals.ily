%%%install HEJI in liypond itself
%%%read pdf for character associations.
%%% tempered flat %%%
tempered-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "HEJI")
                "a"
            }
        $note #})

%%% HEJI numbres test %%%
heji-numbers-test =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "HEJI")
                "1 ! 2 @ 3 # 4 $ 5 % 6 ^ 7 & 8 * 9 ( 0 )"
            }
        $note #})

%%% HEJI qwerty test %%%
heji-qwerty-test =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "HEJI")
                "q Q w W e E r R t T y Y u U i I o O p P"
            }
        $note #})

%%% HEJI asdf test %%%
heji-asdf-test =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "HEJI")
                "a A s S d D f F g G h H j J k K l L ; : ' "
            }
        $note #})

%%% zxc asdf test %%%
heji-zxc-test =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "HEJI")
                "z Z x X c C v V b B n N m M , < . > / ?"
            }
        $note #})


%%% ekmelos test %%%
ekmelos-test =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
        #ly:text-interface::print
        \once \override Voice.Accidental.text =
            \markup {
                \fontsize #4
                \override #'(font-name . "ekmelos")
                \char ##xe2e5
            }
        $note #})
