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

#(define-public (open-paren-stencils grob)
  (let ((lp (grob-interpret-markup grob (markup #:fontsize 3.5 #:translate (cons -0.3 -0.5) "(")))
        (rp (grob-interpret-markup grob (markup #:fontsize 3.5 #:translate (cons -0.3 -0.5) ""))))
    (list lp rp)))

#(define-public (close-paren-stencils grob)
  (let ((lp (grob-interpret-markup grob (markup #:fontsize 3.5 #:translate (cons -0.3 -0.5) "")))
        (rp (grob-interpret-markup grob (markup #:fontsize 3.5 #:translate (cons -0.3 -0.5) ")"))))
    (list lp rp)))

open-paren = #(define-music-function (arg) (ly:music?)
   (_i "Tag @var{arg} to be parenthesized.")
#{
  \once \override Parentheses.stencils = #open-paren-stencils
  \parenthesize $arg
#})

close-paren = #(define-music-function (arg) (ly:music?)
   (_i "Tag @var{arg} to be parenthesized.")
#{
  \once \override Parentheses.stencils = #close-paren-stencils
  \parenthesize $arg
#})

suggest-pitch-open = #(define-music-function (note) (ly:music?)
#{
	\once \override Stem.stencil = ##f
    \once \override Beam.stencil = ##f
    \once \override Flag.stencil = ##f
    \open-paren
	$note
#})
suggest-pitch-middle = #(define-music-function (note) (ly:music?)
#{
    \once \override Stem.stencil = ##f
    \once \override Beam.stencil = ##f
    \once \override Flag.stencil = ##f
	$note
#})
suggest-pitch-close = #(define-music-function (note) (ly:music?)
#{
    \once \override Stem.stencil = ##f
    \once \override Beam.stencil = ##f
    \once \override Flag.stencil = ##f
    \close-paren
	$note
#})


%%% rebecca saunders string contact point %%%

start-graphic-scp = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "graphicSCP"
    )

stop-graphic-scp = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "graphicSCP"
    )

%%% interruptive polyphony %%%
% don't forget
% \consists Grob_pq_engraver
% \consists #Interrupt_heads_engraver

#(define (make-butt-line-stencil width start-x start-y end-x end-y)
   (let ((path `(moveto ,start-x ,start-y lineto ,end-x ,end-y)))
     (make-path-stencil path width 1 1 #t #:line-cap-style 'butt)))

#(define (interrupting-bracket grob)
   (let* ((left (ly:spanner-bound grob LEFT))
          (right (ly:spanner-bound grob RIGHT))
          (sys (ly:grob-system grob))
          (start-x (interval-end (ly:grob-extent left sys X)))
          (start-y (interval-center (ly:grob-extent left sys Y)))
          (right-stem (ly:grob-object right 'stem))
          (right-stem-dir (ly:grob-property right-stem 'direction))
          (right-head (reduce (lambda (head prev)
                                (if ((if (eqv? UP right-stem-dir) not identity)
                                     (ly:grob-vertical<? head prev))
                                    head
                                    prev))
                              'dummy
                              (ly:grob-array->list (ly:grob-object right 'note-heads))))
          (end-x (interval-index (interval-widen (ly:grob-extent right-head sys X) -0.07)
                                 (- right-stem-dir)))
          (end-y (interval-center (ly:grob-extent right-head sys Y))))
     (ly:stencil-translate
      (ly:stencil-add
       (make-butt-line-stencil 0.5 (- start-x 0.2) start-y (+ end-x 0.05) start-y)
       (make-butt-line-stencil 0.1 end-x start-y end-x end-y))
      (cons (- (ly:grob-relative-coordinate grob sys X))
            (- (ly:grob-relative-coordinate grob sys Y))))))

#(define (Interrupt_heads_engraver context)
   (let ((interrupted (make-hash-table)))
     (make-engraver
      (acknowledgers
       ((note-column-interface engraver grob source-engraver)
        (when (not (ly:grob-object grob 'rest #f))
          (for-each
           (match-lambda
            ((mom . elt)
             (when (and (grob::has-interface elt 'note-head-interface)
                        (assoc-get 'interrupt (ly:grob-property elt 'details '()))
                        (not (hashq-ref interrupted elt))
                        (not (equal? mom (ly:context-current-moment context))))
               (hashq-set! interrupted elt #t)
               (let ((follower (ly:engraver-make-grob engraver 'VoiceFollower '())))
                 (ly:spanner-set-bound! follower LEFT elt)
                 (ly:spanner-set-bound! follower RIGHT grob)
                 (ly:grob-set-property! follower 'color (assoc-get 'interrupt-color (ly:grob-property elt 'details '())))
                 (ly:grob-set-property! follower 'stencil interrupting-bracket)))))
           (ly:context-property context 'busyGrobs))))))))

interrupt = \once \override Staff.NoteHead.details.interrupt = ##t


%%% explicit interruption %%%

#(define (Explicit_interrupt_heads_engraver context)
  (let ((explicit-interrupted (make-hash-table)))
    (make-engraver
     (acknowledgers
      ((note-column-interface engraver grob source-engraver)
       (when
           (assoc-get 'explicit-interruptible (ly:grob-property grob 'details '()))
         (for-each
          (match-lambda
           ((mom . elt)
            (when (and
                       (assoc-get 'explicit-interrupt (ly:grob-property elt 'details '()))
                       (not (hashq-ref explicit-interrupted elt))
                       )
              (hashq-set! explicit-interrupted elt #t)
              (let ((follower (ly:engraver-make-grob engraver 'VoiceFollower '())))
                (ly:spanner-set-bound! follower LEFT elt)
                (ly:spanner-set-bound! follower RIGHT grob)
                (ly:grob-set-property! follower 'color (assoc-get 'interrupt-color (ly:grob-property elt 'details '())))
                (ly:grob-set-property! follower 'stencil interrupting-bracket)
                ))
           ))
          (ly:context-property context 'busyGrobs))))))))

start-explicit-interrupt = \once \override Staff.NoteHead.details.explicit-interrupt = ##t
stop-explicit-interrupt = \once \override Staff.NoteColumn.details.explicit-interruptible = ##t


%%% hocket lines %%%
% don't forget
% \consists Grob_pq_engraver
% \consists #Hocket_lines_engraver

#(define (Hocket_lines_engraver context)
   (let ((hocketed (make-hash-table)))
     (make-engraver
      (acknowledgers
       ((note-column-interface engraver grob source-engraver)
        (when (not (ly:grob-object grob 'rest #f))
          (for-each
           (match-lambda
            ((mom . elt)
             (when (and (grob::has-interface elt 'note-head-interface)
                        (assoc-get 'hocket (ly:grob-property elt 'details '()))
                        (not (hashq-ref hocketed elt))
                        (not (equal? mom (ly:context-current-moment context))))
               (hashq-set! hocketed elt #t)
               (let ((follower (ly:engraver-make-grob engraver 'VoiceFollower '())))
                 (ly:spanner-set-bound! follower LEFT elt)
                 (ly:spanner-set-bound! follower RIGHT grob)
                 (ly:grob-set-property! follower 'color (assoc-get 'hocket-color (ly:grob-property elt 'details '())))
                 ))
            ))
           (ly:context-property context 'busyGrobs))))))))

hocket = \once \override Staff.NoteHead.details.hocket = ##t

%{ hocket-blue = \once \override Staff.NoteHead.details.hocket-blue = ##t %}
%{ hocket-red = \once \override Staff.NoteHead.details.hocket-red = ##t %}
%{ hocket-green = \once \override Staff.NoteHead.details.hocket-green = ##t %}

%%% line follower (different than hocket) %%%
#(define (Follow_lines_engraver context)
   (let ((followed (make-hash-table)))
     (make-engraver
      (acknowledgers
       ((note-column-interface engraver grob source-engraver)
       ;(format #t "\n\nnote colum grob details: ~A \n\n"  (ly:grob-property grob 'details '()))
        (when
            (assoc-get 'followable (ly:grob-property grob 'details '()))
          (for-each
           (match-lambda
            ((mom . elt)
             (when (and (grob::has-interface elt 'note-head-interface)
                        (assoc-get 'follow (ly:grob-property elt 'details '()))
                        (not (hashq-ref followed elt))
                        )
               (hashq-set! followed elt #t)
               (let ((follower (ly:engraver-make-grob engraver 'VoiceFollower '())))
                 (ly:spanner-set-bound! follower LEFT elt)
                 (ly:spanner-set-bound! follower RIGHT grob)
                 (ly:grob-set-property! follower 'color (assoc-get 'follow-color (ly:grob-property elt 'details '())))
                 ))
            ))
           (ly:context-property context 'busyGrobs))))))))

start-follow = \once \override Staff.NoteHead.details.follow = ##t
stop-follow = \once \override Staff.NoteColumn.details.followable = ##t


%%% Mahnkopf stream switches
#(define (make-switch-butt-line-stencil width start-x start-y end-x end-y)
   (let ((path `(moveto ,start-x ,start-y lineto ,end-x ,end-y)))
     (make-path-stencil path width 1 1 #t #:line-cap-style 'butt)))

#(define (switching-bracket grob)
   (let* ((left (ly:spanner-bound grob LEFT))
          (right (ly:spanner-bound grob RIGHT))
          (x-proportion (assoc-get 'used-proportion (ly:grob-property grob 'details '())))
          (sys (ly:grob-system grob))
          (start-x (interval-end (ly:grob-extent left sys X)))
          (start-y (interval-center (ly:grob-extent left sys Y)))
          (right-stem (ly:grob-object right 'stem))
          (right-stem-dir (ly:grob-property right-stem 'direction))
          (right-head (reduce (lambda (head prev)
                                (if ((if (eqv? UP right-stem-dir) not identity)
                                     (ly:grob-vertical<? head prev))
                                    head
                                    prev))
                              'dummy
                              (ly:grob-array->list (ly:grob-object right 'note-heads))))
          (end-x (interval-index (interval-widen (ly:grob-extent right-head sys X) -0.07)
                                 (- right-stem-dir)))
          (x-distance-total (- end-x start-x))
          (x-distance-proportion (* x-distance-total x-proportion))
          (new-calculated-end-x (+ start-x x-distance-proportion))
          (end-y (interval-center (ly:grob-extent right-head sys Y))))
     (ly:stencil-translate
      (ly:stencil-add
       (make-switch-butt-line-stencil 0.5 (- start-x 0.2) start-y (+ new-calculated-end-x 0.05) start-y)
       (make-switch-butt-line-stencil 0.1 new-calculated-end-x start-y new-calculated-end-x end-y)
       (make-switch-butt-line-stencil 0.5 (- new-calculated-end-x 0.05) end-y end-x end-y)
       )
      (cons (- (ly:grob-relative-coordinate grob sys X))
            (- (ly:grob-relative-coordinate grob sys Y))))))

#(define (Switch_heads_engraver context)
   (let ((switched (make-hash-table)))
     (make-engraver
      (acknowledgers
       ((note-column-interface engraver grob source-engraver)
        (when (assoc-get 'switchable (ly:grob-property grob 'details '()))
          (for-each
           (match-lambda
            ((mom . elt)
             (when (and (grob::has-interface elt 'note-head-interface)
                        (assoc-get 'switch (ly:grob-property elt 'details '()))
                        (not (hashq-ref switched elt))
                        )
               (hashq-set! switched elt #t)
               (let ((follower (ly:engraver-make-grob engraver 'VoiceFollower '())))
                 (ly:spanner-set-bound! follower LEFT elt)
                 (ly:spanner-set-bound! follower RIGHT grob)
                 (ly:grob-set-property! follower 'color (assoc-get 'switch-color (ly:grob-property elt 'details '())))
                 (ly:grob-set-property! follower 'stencil switching-bracket)
                 ))))
           (ly:context-property context 'busyGrobs))))))))

start-switch = #(
    define-music-function
    (proportion)
    (number?)
    #{
    \override StaffGroup.VoiceFollower.details.used-proportion = #proportion
    \once \override Staff.NoteHead.details.switch = ##t
    #}
    )
stop-switch = \once \override Staff.NoteColumn.details.switchable = ##t


%%% duplicate symbol spanners %%%
#(define (make-duplicate-stencil grob amount width markup)
  (let* ((orig (ly:grob-original grob))
         (siblings (if (ly:grob? orig) (ly:spanner-broken-into orig) '()))
         ;; length of the actual grob
         (xspan (grob-width grob))
         ;; add the length of all siblings
         (total-span
           (if (null? siblings)
               (grob-width grob)
               (reduce + 0 (map (lambda (g) (grob-width g)) siblings))))
           (part-size (/ total-span amount))
           (scale-size (/ part-size width))
         ;; get the x-position for the start
         (left-bound
           (if (or (null? siblings) (eq? (car siblings) grob))
               ;; compensate thickness of the line
               ;; start a little left
               (1- (assoc-get 'X (ly:grob-property grob 'left-bound-info)))))
         ;; get the length of the already done parts of the wavy line
         (span-so-far
           (if (null? siblings)
               0
               (-
                 (reduce + 0
                   (map
                     (lambda (g) (grob-width g))
                     (member grob (reverse siblings))))
                 xspan)))
         ;; process the final stencil
         (final-stencil
             (let (
                 (stil (ly:stencil-scale (grob-interpret-markup grob markup) scale-size 1))
                 )
               (let loop ((count (1- amount)) (new-stil stil))
                 (if (> count 0)
                     (loop (1- count)
                           (ly:stencil-combine-at-edge new-stil X LEFT stil 0))
                     (ly:stencil-aligned-to new-stil X LEFT)
                     )
                     )
              )
             )
         (bound-details
           (ly:grob-property grob 'bound-details))
         ;; bound-details.left.padding affects both broken and unbroken spanner
         ;; whereas bound-details.left-broken.padding only affects the broken
         ;; spanner part (same for right and right-broken)
         ;; We need to move the stencil along x-axis if padding is inserted to
         ;; the left
         (x-offset
           (cond
             ((or (null? siblings) (equal? grob (car siblings)))
               (assoc-get 'padding (assoc-get 'left bound-details '()) 0))
             ((member grob siblings)
               ;; get at least one working value for the offset
               (or (assoc-get
                     'padding
                     (assoc-get 'left-broken bound-details '())
                     #f)
                   (assoc-get 'padding (assoc-get 'left bound-details '()) 0)))
             (else 0))))

      (ly:stencil-translate-axis
        final-stencil
        ;; TODO
        ;; there's a little inconsistency here, with the need to add some
        ;; correction, i.e. (* thick 2)
        (if (zero? x-offset)
            0
            (- x-offset (* thick 2)))
        X)))

duplicate-spanner =
#(define-music-function (amount width markup) (number? number? markup?)
#{
\once \override TrillSpanner.after-line-breaking =
#(lambda (grob)
   (ly:grob-set-property! grob 'stencil
     (make-duplicate-stencil grob amount width markup)))
#})

loop-spanner =
#(define-music-function (amount) (number?)
#{
\duplicate-spanner #amount 0.87 \loop-element
#})

square-spanner =
#(define-music-function (amount) (number?)
#{
\duplicate-spanner #amount 1.3 \square-element
#})

random-spanner =
#(define-music-function (amount) (number?)
#{
\duplicate-spanner #amount 2.1 \random-element
#})

random-spanner-two =
#(define-music-function (amount) (number?)
#{
\duplicate-spanner #amount 2.1 \random-element-two
#})

random-spanner-three =
#(define-music-function (amount) (number?)
#{
\duplicate-spanner #amount 3.5 \random-element-three
#})

%%% spanner line styles %%%

evans-dashed-line-with-hook-and-arrow = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak arrow-width 0.25
    - \tweak dash-fraction 0.25
    - \tweak dash-period 1.5
    - \tweak bound-details.left.stencil-align-dir-y #up
    - \tweak bound-details.left-broken.text ##f
    - \tweak bound-details.left.text \markup { \draw-line #'(0 . -1) }
    % right padding to avoid last leaf in spanner:
    %%%- \tweak bound-details.right.padding 1.25
    - \tweak bound-details.right.stencil-align-dir-y #center
    - \tweak bound-details.right.arrow ##t
    - \tweak bound-details.right-broken.arrow ##t
    - \tweak bound-details.right.padding 0.5
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )


evans-solid-line-with-hook-and-arrow = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak arrow-width 0.25
    - \tweak dash-fraction 1
    - \tweak bound-details.left.stencil-align-dir-y #up
    - \tweak bound-details.left-broken.text ##f
    - \tweak bound-details.left.text \markup { \draw-line #'(0 . -1) }
    % right padding to avoid last leaf in spanner:
    %%%- \tweak bound-details.right.padding 1.25
    - \tweak bound-details.right.stencil-align-dir-y #center
    - \tweak bound-details.right.arrow ##t
    - \tweak bound-details.right-broken.arrow ##t
    - \tweak bound-details.right.padding 0.5
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )


%%% variable trills %%%
%\once \override TrillSpanner.thickness = 3
%\once \override TrillSpanner.details.squiggle-initial-width = 0.4
%\once \override TrillSpanner.details.squiggle-Y-scale = 0.8
%% Use a negative value for a fast-slow trill.
%% Bad things will happen if you set this to 1 or more!
%\once \override TrillSpanner.details.squiggle-speed-factor = -0.6

slow-fast-trill =
\tweak TrillSpanner.stencil
#(lambda (grob)
    (let* ((left (ly:spanner-bound grob LEFT))
           (right (ly:spanner-bound grob RIGHT))
           (sys (ly:grob-system grob))
           (my-coord (ly:grob-relative-coordinate grob sys X))
           (trill-start-x (interval-start (ly:grob-extent left sys X)))
           (glyph-stil
            (ly:stencil-translate-axis
             (ly:stencil-aligned-to
              (grob-interpret-markup
               grob
               #{ \markup \general-align #Y #CENTER \musicglyph
"scripts.trill" #})
              X
              LEFT)
             trill-start-x
             X))
           (squiggle-glyph-stil
            (grob-interpret-markup
             grob
             #{ \markup \lower #0.6 \general-align #X #LEFT \musicglyph
"scripts.trill_element" #}))
           (squiggle-glyph-width (interval-length (ly:stencil-extent
squiggle-glyph-stil X)))
           (start-x (+ (interval-end (ly:stencil-extent glyph-stil X))
                       0.8))
           (end-x (- (interval-start (ly:grob-extent right sys X)) 3.55)) ;; originally no subtraction
           (thickness (* (ly:grob-property grob 'thickness 2.0)
                         (ly:staff-symbol-line-thickness grob)))
           (det (ly:grob-property grob 'details))
           (squiggle-height (assoc-get 'squiggle-height det 0.3))
           (squiggle-initial-width (assoc-get 'squiggle-initial-width
det 2.0))
           (squiggle-speed-factor (assoc-get 'squiggle-speed-factor det
0.4))
           (squiggle-Y-scale (assoc-get 'squiggle-Y-scale det 0.55)))
      (let loop ((x start-x)
                 (dir UP)
                 (i 1)
                 (stil glyph-stil))
        (if (>= x end-x)
            (ly:stencil-translate-axis stil (- my-coord) X)
            (let ((width (* squiggle-initial-width (/ (expt i
squiggle-speed-factor)))))
              (loop (+ x width)
                    (- dir)
                    (1+ i)
                    (let ((squiggle (ly:stencil-translate-axis
                                     (ly:stencil-scale squiggle-glyph-stil
                                                       (/ width
squiggle-glyph-width)
squiggle-Y-scale)
                                     x
                                     X)))
                      (ly:stencil-add stil squiggle))))))))
\startTrillSpan


slow-fast-harmonic =
\tweak TrillSpanner.stencil
#(lambda (grob)
    (let* ((left (ly:spanner-bound grob LEFT))
           (right (ly:spanner-bound grob RIGHT))
           (sys (ly:grob-system grob))
           (my-coord (ly:grob-relative-coordinate grob sys X))
           (trill-start-x (interval-start (ly:grob-extent left sys X)))
           (glyph-stil
            (ly:stencil-translate-axis
             (ly:stencil-aligned-to
              (grob-interpret-markup
               grob
               #{ \markup \general-align #Y #CENTER \musicglyph
"noteheads.s0harmonic" #})
              X
              LEFT)
             trill-start-x
             X))
           (squiggle-glyph-stil
            (grob-interpret-markup
             grob
             #{ \markup \lower #0.6 \general-align #X #LEFT \musicglyph
"scripts.trill_element" #}))
           (squiggle-glyph-width (interval-length (ly:stencil-extent
squiggle-glyph-stil X)))
           (start-x (+ (interval-end (ly:stencil-extent glyph-stil X))
                       0.8))
           (end-x (- (interval-start (ly:grob-extent right sys X)) 3.55)) ;; originally no subtraction
           (thickness (* (ly:grob-property grob 'thickness 2.0)
                         (ly:staff-symbol-line-thickness grob)))
           (det (ly:grob-property grob 'details))
           (squiggle-height (assoc-get 'squiggle-height det 0.3))
           (squiggle-initial-width (assoc-get 'squiggle-initial-width
det 2.0))
           (squiggle-speed-factor (assoc-get 'squiggle-speed-factor det
0.4))
           (squiggle-Y-scale (assoc-get 'squiggle-Y-scale det 0.55)))
      (let loop ((x start-x)
                 (dir UP)
                 (i 1)
                 (stil glyph-stil))
        (if (>= x end-x)
            (ly:stencil-translate-axis stil (- my-coord) X)
            (let ((width (* squiggle-initial-width (/ (expt i
squiggle-speed-factor)))))
              (loop (+ x width)
                    (- dir)
                    (1+ i)
                    (let ((squiggle (ly:stencil-translate-axis
                                     (ly:stencil-scale squiggle-glyph-stil
                                                       (/ width
squiggle-glyph-width)
squiggle-Y-scale)
                                     x
                                     X)))
                      (ly:stencil-add stil squiggle))))))))
\startTrillSpan


slow-fast-bisbigliando =
\tweak TrillSpanner.stencil
#(lambda (grob)
    (let* ((left (ly:spanner-bound grob LEFT))
           (right (ly:spanner-bound grob RIGHT))
           (sys (ly:grob-system grob))
           (my-coord (ly:grob-relative-coordinate grob sys X))
           (trill-start-x (interval-start (ly:grob-extent left sys X)))
           (glyph-stil
            (ly:stencil-translate-axis
             (ly:stencil-aligned-to
              (grob-interpret-markup
               grob
               #{ \markup \general-align #Y #CENTER "bis" #})
              X
              LEFT)
             trill-start-x
             X))
           (squiggle-glyph-stil
            (grob-interpret-markup
             grob
             #{ \markup \lower #0.6 \general-align #X #LEFT \musicglyph
"scripts.trill_element" #}))
           (squiggle-glyph-width (interval-length (ly:stencil-extent
squiggle-glyph-stil X)))
           (start-x (+ (interval-end (ly:stencil-extent glyph-stil X))
                       0.8))
           (end-x (- (interval-start (ly:grob-extent right sys X)) 3.55)) ;; originally no subtraction
           (thickness (* (ly:grob-property grob 'thickness 2.0)
                         (ly:staff-symbol-line-thickness grob)))
           (det (ly:grob-property grob 'details))
           (squiggle-height (assoc-get 'squiggle-height det 0.3))
           (squiggle-initial-width (assoc-get 'squiggle-initial-width
det 2.0))
           (squiggle-speed-factor (assoc-get 'squiggle-speed-factor det
0.4))
           (squiggle-Y-scale (assoc-get 'squiggle-Y-scale det 0.55)))
      (let loop ((x start-x)
                 (dir UP)
                 (i 1)
                 (stil glyph-stil))
        (if (>= x end-x)
            (ly:stencil-translate-axis stil (- my-coord) X)
            (let ((width (* squiggle-initial-width (/ (expt i
squiggle-speed-factor)))))
              (loop (+ x width)
                    (- dir)
                    (1+ i)
                    (let ((squiggle (ly:stencil-translate-axis
                                     (ly:stencil-scale squiggle-glyph-stil
                                                       (/ width
squiggle-glyph-width)
squiggle-Y-scale)
                                     x
                                     X)))
                      (ly:stencil-add stil squiggle))))))))
\startTrillSpan


slow-fast-flute-heel =
\tweak TrillSpanner.stencil
#(lambda (grob)
    (let* ((left (ly:spanner-bound grob LEFT))
           (right (ly:spanner-bound grob RIGHT))
           (sys (ly:grob-system grob))
           (my-coord (ly:grob-relative-coordinate grob sys X))
           (trill-start-x (interval-start (ly:grob-extent left sys X)))
           (glyph-stil
            (ly:stencil-translate-axis
             (ly:stencil-aligned-to
              (grob-interpret-markup
               grob
               #{ \markup \general-align #Y #CENTER \concat { "(" \raise #0.5 \rotate #50 \musicglyph "scripts.upedalheel" \raise #0.75 \override #'(font-size . -3) \arrow-head #X #LEFT ##f \raise #0.75 \draw-line #'(-0.75 . 0) \raise #0.75 \override #'(font-size . -3) \arrow-head #X #RIGHT ##f \raise #0.5 \rotate #-50 \musicglyph "scripts.upedalheel" ")" } #})
              X
              LEFT)
             trill-start-x
             X))
           (squiggle-glyph-stil
            (grob-interpret-markup
             grob
             #{ \markup \lower #0.6 \general-align #X #LEFT \musicglyph
"scripts.trill_element" #}))
           (squiggle-glyph-width (interval-length (ly:stencil-extent
squiggle-glyph-stil X)))
           (start-x (+ (interval-end (ly:stencil-extent glyph-stil X))
                       0.8))
           (end-x (- (interval-start (ly:grob-extent right sys X)) 3.55)) ;; originally no subtraction
           (thickness (* (ly:grob-property grob 'thickness 2.0)
                         (ly:staff-symbol-line-thickness grob)))
           (det (ly:grob-property grob 'details))
           (squiggle-height (assoc-get 'squiggle-height det 0.3))
           (squiggle-initial-width (assoc-get 'squiggle-initial-width
det 2.0))
           (squiggle-speed-factor (assoc-get 'squiggle-speed-factor det
0.4))
           (squiggle-Y-scale (assoc-get 'squiggle-Y-scale det 0.55)))
      (let loop ((x start-x)
                 (dir UP)
                 (i 1)
                 (stil glyph-stil))
        (if (>= x end-x)
            (ly:stencil-translate-axis stil (- my-coord) X)
            (let ((width (* squiggle-initial-width (/ (expt i
squiggle-speed-factor)))))
              (loop (+ x width)
                    (- dir)
                    (1+ i)
                    (let ((squiggle (ly:stencil-translate-axis
                                     (ly:stencil-scale squiggle-glyph-stil
                                                       (/ width
squiggle-glyph-width)
squiggle-Y-scale)
                                     x
                                     X)))
                      (ly:stencil-add stil squiggle))))))))
\startTrillSpan

 slow-fast-smorzando =
 \tweak TrillSpanner.stencil
 #(lambda (grob)
     (let* ((left (ly:spanner-bound grob LEFT))
            (right (ly:spanner-bound grob RIGHT))
            (sys (ly:grob-system grob))
            (my-coord (ly:grob-relative-coordinate grob sys X))
            (trill-start-x (interval-start (ly:grob-extent left sys X)))
            (glyph-stil
             (ly:stencil-translate-axis
              (ly:stencil-aligned-to
               (grob-interpret-markup
                grob
                #{ \markup \general-align #Y #CENTER \fontsize #-3 "smz." #})
               X
               LEFT)
              trill-start-x
              X))
            (squiggle-glyph-stil
             (grob-interpret-markup
              grob
              #{ \markup \lower #0.6 \general-align #X #LEFT \override #'(font-name . "ekmelos") \char ##xeab8
 #}))
            (squiggle-glyph-width (interval-length (ly:stencil-extent
 squiggle-glyph-stil X)))
            (start-x (+ (interval-end (ly:stencil-extent glyph-stil X))
                        0.8))
            (end-x (- (interval-start (ly:grob-extent right sys X)) 3.55)) ;; originally no subtraction
            (thickness (* (ly:grob-property grob 'thickness 2.0)
                          (ly:staff-symbol-line-thickness grob)))
            (det (ly:grob-property grob 'details))
            (squiggle-height (assoc-get 'squiggle-height det 0.3))
            (squiggle-initial-width (assoc-get 'squiggle-initial-width
 det 2.0))
            (squiggle-speed-factor (assoc-get 'squiggle-speed-factor det
 0.4))
            (squiggle-Y-scale (assoc-get 'squiggle-Y-scale det 0.55)))
       (let loop ((x start-x)
                  (dir UP)
                  (i 1)
                  (stil glyph-stil))
         (if (>= x end-x)
             (ly:stencil-translate-axis stil (- my-coord) X)
             (let ((width (* squiggle-initial-width (/ (expt i
 squiggle-speed-factor)))))
               (loop (+ x width)
                     (- dir)
                     (1+ i)
                     (let ((squiggle (ly:stencil-translate-axis
                                      (ly:stencil-scale squiggle-glyph-stil
                                                        (/ width
 squiggle-glyph-width)
 squiggle-Y-scale)
                                      x
                                      X)))
                       (ly:stencil-add stil squiggle))))))))
 \startTrillSpan


 slow-fast-circle =
 \tweak TrillSpanner.stencil
 #(lambda (grob)
     (let* ((left (ly:spanner-bound grob LEFT))
            (right (ly:spanner-bound grob RIGHT))
            (sys (ly:grob-system grob))
            (my-coord (ly:grob-relative-coordinate grob sys X))
            (trill-start-x (interval-start (ly:grob-extent left sys X)))
            (glyph-stil
             (ly:stencil-translate-axis
              (ly:stencil-aligned-to
               (grob-interpret-markup
                grob
                #{ \markup \general-align #Y #CENTER \fontsize #-3 "cir." #})
               X
               LEFT)
              trill-start-x
              X))
            (squiggle-glyph-stil
             (grob-interpret-markup
              grob
              #{ \markup \lower #0.6 \general-align #X #LEFT \override #'(font-name . "ekmelos") \char ##xeac3
 #}))
            (squiggle-glyph-width (interval-length (ly:stencil-extent
 squiggle-glyph-stil X)))
            (start-x (+ (interval-end (ly:stencil-extent glyph-stil X))
                        0.8))
            (end-x (- (interval-start (ly:grob-extent right sys X)) 3.55)) ;; originally no subtraction
            (thickness (* (ly:grob-property grob 'thickness 2.0)
                          (ly:staff-symbol-line-thickness grob)))
            (det (ly:grob-property grob 'details))
            (squiggle-height (assoc-get 'squiggle-height det 0.3))
            (squiggle-initial-width (assoc-get 'squiggle-initial-width
 det 2.0))
            (squiggle-speed-factor (assoc-get 'squiggle-speed-factor det
 0.4))
            (squiggle-Y-scale (assoc-get 'squiggle-Y-scale det 0.55)))
       (let loop ((x start-x)
                  (dir UP)
                  (i 1)
                  (stil glyph-stil))
         (if (>= x end-x)
             (ly:stencil-translate-axis stil (- my-coord) X)
             (let ((width (* squiggle-initial-width (/ (expt i
 squiggle-speed-factor)))))
               (loop (+ x width)
                     (- dir)
                     (1+ i)
                     (let ((squiggle (ly:stencil-translate-axis
                                      (ly:stencil-scale squiggle-glyph-stil
                                                        (/ width
 squiggle-glyph-width)
 squiggle-Y-scale)
                                      x
                                      X)))
                       (ly:stencil-add stil squiggle))))))))
 \startTrillSpan


 %%% GRAPHIC BOW PRESSURE %%%

startGraphicBowPressure = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "GraphicBP"
)

stopGraphicBowPressure = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "GraphicBP"
)

#(define ((bow-pressure-stencil shape) grob)
  (let* ((lbi (ly:grob-property grob 'left-bound-info '()))
         (rbi (ly:grob-property grob 'right-bound-info '()))
         (lbx (ly:assoc-get 'X lbi 0))
         (rbx (ly:assoc-get 'X rbi 0))
         (ss (ly:staff-symbol-staff-space grob)))
    (set! shape (append '((1 . 0) (0 . 0)) shape))
    (set! shape
      (map
        (lambda (pt) (let ((x (car pt)) (y (cdr pt)))
          (cons (* x (- rbx lbx)) (* -2/3 ss y))))
        shape))
    (grob-interpret-markup grob
      #{ \markup \polygon #shape #})))

startBowSpan =
    #(define-event-function (shape) (number-pair-list?) #{
      -\tweak stencil #(bow-pressure-stencil shape)
       \startGraphicBowPressure #})

stopBowSpan = \stopGraphicBowPressure
