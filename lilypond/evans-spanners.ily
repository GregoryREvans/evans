\version "2.23.14" % temp
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

%%% color phrasing slur spanner %%%

color-span =
#(define-music-function (parser location y-lower y-upper color)
     (number? number? color?)
    #{
      \once\override PhrasingSlur.stencil =
        $(lambda (grob)
          (let* (
            (area (ly:slur::print grob))
              (X-ext (ly:stencil-extent area X))
              (Y-ext (ly:stencil-extent area Y)))
            (set! Y-ext (cons y-lower y-upper))
            (ly:grob-set-property! grob 'layer -10)
            (ly:make-stencil (list 'color color
              (ly:stencil-expr (ly:round-filled-box X-ext Y-ext 0))
              X-ext Y-ext))))
      \once\override PhrasingSlur.Y-offset = #0
    #})

%%% Haupt and Neben stimmen %%%

hauptStart = \markup {
  \path #0.25 #'((moveto 0 0)
                 (lineto 0 -2)
                 (moveto 0 -1)
                 (lineto 1 -1)
                 (moveto 1 0)
                 (lineto 1 -2)
                 (moveto 1 0)
                 (lineto 1.8 0))
}

nebenStart = \markup {
  \path #0.25 #'((moveto 0 -2)
                 (lineto 0 0)
                 (lineto 1 -2)
                 (lineto 1 0)
                 (lineto 1.8 0))
}

stimmeStop = \markup {
  \path #0.25 #'((moveto 0 0)
                 (lineto 0.8 0)
                 (lineto 0.8 -0.8))
}

hauptStimmeStart =
#(define-music-function (parser location )()
#{
          \once \override TextSpanner.before-line-breaking =
              #(lambda (grob)
                  (let* ((sz (ly:grob-property grob 'font-size 0.0))
                         (mult (magstep sz)))
                  (begin
                     (ly:grob-set-property! grob 'style 'none)
                     (ly:grob-set-nested-property! grob
                               '(bound-details left text)
                                  (markup #:scale (cons mult mult) hauptStart))
                     (ly:grob-set-nested-property! grob
                               '(bound-details right text)
                                  (markup #:scale (cons mult mult) stimmeStop))
                     ;;Perhaps you may want to uncomment the following lines
                     ;;and adjust the value (currently -0.5)
                     ;;(ly:grob-set-nested-property! grob
                     ;;          '(bound-details right padding) -0.5)
                     (ly:grob-set-nested-property! grob
                               '(bound-details left-broken text) #f)
                     (ly:grob-set-nested-property! grob
                               '(bound-details right-broken text) #f))))
          $(make-music 'EventChord 'elements (list
          		               (make-music
          		                 'TextSpanEvent
          		                 'span-direction -1)))
#})

nebenStimmeStart =
#(define-music-function (parser location )()
#{
          \once \override TextSpanner.before-line-breaking =
              #(lambda (grob)
                  (let* ((sz (ly:grob-property grob 'font-size 0.0))
                         (mult (magstep sz)))
                  (begin
                     (ly:grob-set-property! grob 'style 'none)
                     (ly:grob-set-nested-property! grob
                               '(bound-details left text)
                                  (markup #:scale (cons mult mult) nebenStart))
                     (ly:grob-set-nested-property! grob
                               '(bound-details right text)
                                  (markup #:scale (cons mult mult) stimmeStop))
                     ;;Perhaps you may want to uncomment the following lines
                     ;;and adjust the value (currently -0.5)
                     ;;(ly:grob-set-nested-property! grob
                     ;;          '(bound-details right padding) -0.5)
                     (ly:grob-set-nested-property! grob
                               '(bound-details left-broken text) #f)
                     (ly:grob-set-nested-property! grob
                               '(bound-details right-broken text) #f))))
          $(make-music 'EventChord 'elements (list
          		               (make-music
          		                 'TextSpanEvent
          		                 'span-direction -1)))
#})

hauptStimmeStop = \stopTextSpan
nebenStimmeStop = \stopTextSpan


%%% MATERIAL ANNOTATION SPANNER %%%

evansStartTextSpanMaterialAnnotation = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "MaterialAnnotation"
    )

evansStopTextSpanMaterialAnnotation = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "MaterialAnnotation"
    )

%%% RHYTHM ANNOTATION SPANNER %%%

evansStartTextSpanRhythmAnnotation = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "RhythmAnnotation"
    )

evansStopTextSpanRhythmAnnotation = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "RhythmAnnotation"
    )

evans-text-spanner-left-text = #(
    define-music-function
    (parser location string music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \upright #string \hspace #0.5
        }
    $music
    #}
    )


    %%% BCP SPANNER %%%

    bacaStartTextSpanBCP = #(
        make-music 'TextSpanEvent 'span-direction START 'spanner-id "BCP"
        )

    bacaStopTextSpanBCP = #(
        make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "BCP"
        )

    #(define-markup-command
        (baca-bcp-left layout props n d)
        (number? number?)
        (interpret-markup layout props
        #{
        \markup \concat {
            \upright \fraction #(number->string n) #(number->string d)
            \hspace #0.5
            }
        #})
        )

    baca-bcp-spanner-left-text = #(
        define-music-function
        (parser location n d music)
        (number? number? ly:music?)
        #{
        \tweak bound-details.left.text \markup \baca-bcp-left #n #d
        $music
        #}
        )

    #(define-markup-command
        (baca-bcp-right layout props n d)
        (number? number?)
        (interpret-markup layout props
        #{
        \markup \upright \fraction #(number->string n) #(number->string d)
        #})
        )

    baca-bcp-spanner-right-text = #(
        define-music-function
        (parser location n d music)
        (number? number? ly:music?)
        #{
        \tweak bound-details.right.text \markup \baca-bcp-right #n #d
        $music
        #}
        )


%%% FANCY GLISS %%%

lengthen-gliss =
#(define-music-function (nmbr)(number?)
#{
  \once \override Glissando.springs-and-rods = #ly:spanner::set-spacing-rods
  \once \override Glissando.minimum-length = #nmbr
#})


fancy-gliss =
#(define-music-function (pts-list right-padding)(list? number?)
#{
 \once \override Glissando.bound-details.left.padding = 0
 \once \override Glissando.bound-details.left.start-at-dot = ##f
 \once \override Glissando.bound-details.right.padding = #right-padding
 \once \override Glissando.after-line-breaking =
  #(lambda (grob)
    (let ((stil (ly:line-spanner::print grob)))
     (if (ly:stencil? stil)
         (let*
           ((left-bound-info (ly:grob-property grob 'left-bound-info))
            (left-bound (ly:spanner-bound grob LEFT))
            (y-off (assoc-get 'Y left-bound-info))
            (padding (assoc-get 'padding left-bound-info))
            (note-column (ly:grob-parent left-bound X))
            (note-heads (ly:grob-object note-column 'note-heads))
            (ext-X
              (if (null? note-heads)
                  '(0 . 0)
                  (ly:relative-group-extent note-heads grob X)))
            (dot-column (ly:note-column-dot-column note-column))
            (dots
              (if (null? dot-column)
                  '()
                  (ly:grob-object dot-column 'dots)))
            (dots-ext-X
              (if (null? dots)
                  '(0 . 0)
                  (ly:relative-group-extent dots grob X)))
            (factor
              (/ (interval-length (ly:stencil-extent stil X))
                 (car (take-right (last pts-list) 2))))
            (new-stil
              (make-connected-path-stencil
                (map
                  (lambda (e)
                    (cond ((= (length e) 2)
                           (cons (* (car e) factor) (cdr e)))
                          ((= (length e) 6)
                           (list
                             (* (car e) factor)
                             (cadr e)
                             (* (third e) factor)
                             (fourth e)
                             (* (fifth e) factor)
                             (sixth e)))
                          (else
                            (ly:error
                              "Some element(s) of the given list do not fit"))))
                  pts-list)
                (layout-line-thickness grob) ;line-width
                1   ;scaling
                1   ;scaling
                #f
                #f)))
         (ly:grob-set-property! grob 'stencil
           (ly:stencil-translate
            new-stil
            (cons (+ (interval-length ext-X)
                     (interval-length dots-ext-X)
                     padding)
                  y-off))))
       (begin
         (ly:warning
           "Cannot find stencil. Please set 'minimum-length accordingly")
         #f))))
#})

%% comment me
%#(display "\n\tLimitations:
%\t-Does not work with line-break
%\t-dotted notes with glissando may return a warning for unknown reasons,
%\t strange things may happen, if contexts die prematurely")

%% If spacing is very tight Glissando sometimes is omitted.
%% Use 'lengthen-gliss' with an apropiate value in this case.
%\lengthen-gliss #10
%{ \override Glissando.cross-staff = ##t %}


%%% MULTI TRILLS %%%

startDoubleTrillSpanUp = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "DTSUp"
    )

stopDoubleTrillSpanUp = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "DTSUp"
    )

startDoubleTrillSpanDown = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "DTSDn"
    )

stopDoubleTrillSpanDown = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "DTSDn"
    )

startTripleTrillSpanDown = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "TTSDn"
    )

stopTripleTrillSpanDown = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "TTSDn"
    )

startDoubleTrill =
	#(define-music-function (padding1 padding2)(number? number?)
		#{
			- \tweak bound-details.left.text \markup {\hspace #0.5 }
			- \tweak bound-details.left.padding #1
			- \tweak style #'trill
			- \tweak staff-padding #padding1
			- \tweak padding #0
			- \tweak Y-extent #0
			\startDoubleTrillSpanDown
			- \tweak bound-details.left.text \markup {\lower #0.25 \musicglyph "scripts.trill" \hspace #0.5 }
			- \tweak style #'trill
			- \tweak staff-padding #padding2
			- \tweak padding #0
			- \tweak Y-extent #0
			\startDoubleTrillSpanUp
		#}
	)

stopDoubleTrill = \stopDoubleTrillSpanUp \stopDoubleTrillSpanDown

startTripleTrill =
	#(define-music-function (padding1 padding2 padding3)(number? number? number?)
		#{
			- \tweak bound-details.left.text \markup {\hspace #0.5 }
			- \tweak bound-details.left.padding #1
			- \tweak style #'trill
			- \tweak staff-padding #padding1
			- \tweak padding #0
			- \tweak Y-extent #0
			\startDoubleTrillSpanDown
			- \tweak bound-details.left.text \markup {\lower #0.5 \musicglyph "scripts.trill" \hspace #0.5 }
			- \tweak style #'trill
			- \tweak staff-padding #padding2
			- \tweak padding #0
			- \tweak Y-extent #0
			\startDoubleTrillSpanUp
			- \tweak bound-details.left.text \markup {\hspace #0.5 }
			- \tweak bound-details.left.padding #1
			- \tweak style #'trill
			- \tweak staff-padding #padding3
			- \tweak padding #0
			- \tweak Y-extent #0
			\startTripleTrillSpanDown
		#}
	)

stopTripleTrill = \stopDoubleTrillSpanUp \stopDoubleTrillSpanDown \stopTripleTrillSpanDown

suggest-pitch-open = #(define-music-function (note) (ly:music?)
#{
	\once \override TextScript.extra-offset = #'(-1.25 . 1.75)
	\tweak Stem.transparent ##t
	$note
#})
suggest-pitch-middle = #(define-music-function (note) (ly:music?)
#{
	\tweak Stem.transparent ##t
	$note
#})
suggest-pitch-close = #(define-music-function (note) (ly:music?)
#{
	\once \override TextScript.extra-offset = #'(0.75 . 1.75)
	\tweak Stem.transparent ##t
	$note
#})
