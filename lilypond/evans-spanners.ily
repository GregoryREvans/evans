%%% Bow Angle Degree SPANNER %%%

evansStartTextSpanBAD = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "BAD"
    )

evansStopTextSpanBAD = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "BAD"
    )

#(define-markup-command
    (evans-clockwise-BAD-left layout props deg)
    (number?)
    (interpret-markup layout props
    #{
        \markup {
            \concat
                {
                 \evans-clockwise-arc
                \translate #'(0.2 . 0.75)
                \scale #'(0.7 . 0.7)  % was \scale #'(0.4 . 0.4)
                \concat {
                    \translate #'(0 . 0)
                    #(number->string deg)
                    \translate #'(0 . 1)
                    \teeny o
                    \hspace #0.5
                    }
                }
            }
    #})
    )

#(define-markup-command
    (evans-counterclockwise-BAD-left layout props deg)
    (number?)
    (interpret-markup layout props
    #{
        \markup {
            \concat
                {
                 \evans-counterclockwise-arc
                \translate #'(0.2 . 0.75)
                \scale #'(0.7 . 0.7)  % was \scale #'(0.4 . 0.4)
                \concat {
                    \translate #'(0 . 0)
                    #(number->string deg)
                    \translate #'(0 . 1)
                    \teeny o
                    \hspace #0.5
                    }
                }
            }
    #})
    )

evans-clockwise-BAD-spanner-left-text = #(
    define-music-function
    (parser location deg music)
    (number? ly:music?)
    #{
    \tweak bound-details.left.text \markup \evans-clockwise-BAD-left #deg
    $music
    #}
    )

evans-counterclockwise-BAD-spanner-left-text = #(
    define-music-function
    (parser location deg music)
    (number? ly:music?)
    #{
    \tweak bound-details.left.text \markup \evans-counterclockwise-BAD-left #deg
    $music
    #}
    )

#(define-markup-command
    (evans-BAD-right layout props deg)
    (number?)
    (interpret-markup layout props
    #{
        \markup {
            \translate #'(0 . 0.75)
                \scale #'(0.7 . 0.7)  % was \scale #'(0.4 . 0.4)
                \concat {
                    \translate #'(0 . 0)
                    #(number->string deg)
                    \translate #'(0 . 1)
                    \teeny o
                    \hspace #0.5
                    }
            }
    #})
    )

evans-BAD-spanner-right-text = #(
    define-music-function
    (parser location deg music)
    (number? ly:music?)
    #{
    \tweak bound-details.right.text \markup \evans-BAD-right #deg
    $music
    #}
    )

%%% Baca METRONOME MARK SPANNER %%%

bacaStartTextSpanMM = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "MM"
    )

bacaStopTextSpanMM = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "MM"
    )

baca-metronome-mark-spanner-layer = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \tweak extra-offset #'(0 . 6)
    $music
    #}
    )

baca-metronome-mark-spanner-colored-left-markup = #(
    define-music-function
    (parser location markup color music)
    (markup? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        #markup
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-colored-left-text = #(
    define-music-function
    (parser location log dots stem string color music)
    (number? number? number? string? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-metronome-mark-markup #log #dots #stem #string
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-colored-left-text-mixed-number = #(
    define-music-function
    (parser location log dots stem base n d color music)
    (number? number? number? string? string? string? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-metronome-mark-fraction-markup #log #dots #stem #base #n #d
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-left-markup = #(
    define-music-function
    (parser location markup music)
    (markup? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        #markup
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-left-text = #(
    define-music-function
    (parser location log dots stem string music)
    (number? number? number? string? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-metronome-mark-markup #log #dots #stem #string
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-left-text-mixed-number = #(
    define-music-function
    (parser location log dots stem base n d music)
    (number? number? number? string? string? string? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-metronome-mark-mixed-number-markup #log #dots #stem #base #n #d
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-metric-modulation = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale music)
    (number? number? number? string?
        number? number? number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation
            #mm-length #mm-dots #mm-stem #mm-value
            #lhs-length #lhs-dots #rhs-length #rhs-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-mixed-number-metric-modulation = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale music)
    (number? number? number? string? string? string?
        number? number? number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-mixed-number-metric-modulation
            #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            #lhs-length #lhs-dots #rhs-length #rhs-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-metric-modulation = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale color music)
    (number? number? number? string?
        number? number? number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-bracketed-metric-modulation
            #mm-length #mm-dots #mm-stem #mm-value
            #lhs-length #lhs-dots #rhs-length #rhs-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-mixed-number-metric-modulation = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale color music)
    (number? number? number? string? string? string?
        number? number? number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-bracketed-mixed-number-metric-modulation
            #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            #lhs-length #lhs-dots #rhs-length #rhs-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-metric-modulation-tuplet-lhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale music)
    (number? number? number? string?
        number? number? number? number?
        number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation-tuplet-lhs
            #mm-length #mm-dots #mm-stem #mm-value
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #note-length #note-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-mixed-number-metric-modulation-tuplet-lhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale music)
    (number? number? number? string? string? string?
        number? number? number? number?
        number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-mixed-number-metric-modulation-tuplet-lhs
            #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #note-length #note-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-metric-modulation-tuplet-lhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale color music)
    (number? number? number? string?
        number? number? number? number?
        number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation-tuplet-lhs
            #mm-length #mm-dots #mm-stem #mm-value
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #note-length #note-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-mixed-number-metric-modulation-tuplet-lhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale color music)
    (number? number? number? string? string? string?
        number? number? number? number?
        number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-mixed-number-metric-modulation-tuplet-lhs
            #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #note-length #note-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-metric-modulation-tuplet-rhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale music)
    (number? number? number? string?
        number? number?
        number? number? number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation-tuplet-rhs
            #mm-length #mm-dots #mm-stem #mm-value
            #note-length #note-dots
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-mixed-number-metric-modulation-tuplet-rhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale music)
    (number? number? number? string? string? string?
        number? number?
        number? number? number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-mixed-number-metric-modulation-tuplet-rhs
            #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            #note-length #note-dots
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-metric-modulation-tuplet-rhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale color music)
    (number? number? number? string?
        number? number?
        number? number? number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-bracketed-metric-modulation-tuplet-rhs
            #mm-length #mm-dots #mm-stem #mm-value
            #note-length #note-dots
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-mixed-number-metric-modulation-tuplet-rhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale color music)
    (number? number? number? string? string? string?
        number? number?
        number? number? number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-bracketed-mixed-number-metric-modulation-tuplet-rhs
            #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            #note-length #note-dots
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )
