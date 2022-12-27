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
    \open-paren
	$note
#})
suggest-pitch-middle = #(define-music-function (note) (ly:music?)
#{
    \once \override Stem.stencil = ##f
    \once \override Beam.stencil = ##f
	$note
#})
suggest-pitch-close = #(define-music-function (note) (ly:music?)
#{
    \once \override Stem.stencil = ##f
    \once \override Beam.stencil = ##f
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


%%% Ferneyhough Interruptive Polyphony Engraver and Commands %%%
%%% Don't forget \consists #interrupt_heads_engraver in \SCORE
#(define (draw-ps-line length offset thickness)
  (ly:make-stencil (list 'embedded-ps
                   (ly:format "gsave
                    /x ~4f def
                    /offset ~4f def
                    /thickness ~4f def
                    currentpoint translate
                    thickness setlinewidth
                    2 setlinecap
                    2 setlinejoin
                    newpath
                    offset thickness moveto
                    x thickness lineto
                    stroke
                    newpath
                    offset thickness sub thickness -1 mul moveto
                    x thickness -1 mul lineto
                    stroke
                    newpath
                    thickness 2 mul setlinewidth
                    offset 0 moveto
                    x thickness sub 0 lineto
                    stroke
                    grestore
                    " length (- offset 0.015) thickness))
                (cons -0.5 0.5)
                (cons -0.5 0.5))
)

#(define (draw-ps-bracket length offset position thickness)
  (ly:make-stencil (list 'embedded-ps
                   (ly:format "gsave
                    /x ~4f def
                    /offset ~4f def
                    /end-pos ~4f def
                    /thickness ~4f def
                    currentpoint translate
                    newpath
                    thickness setlinewidth
                    2 setlinecap
                    2 setlinejoin
                    offset thickness moveto
                    x thickness lineto
                    x 0 moveto
                    x end-pos lineto
                    stroke
                    newpath
                    offset thickness sub thickness -1 mul moveto
                    x thickness -1 mul lineto
                    stroke
                    newpath
                    thickness 2 mul setlinewidth
                    offset 0 moveto
                    x thickness sub 0 lineto
                    stroke
                    grestore
                    " length (- offset 0.015) position thickness))
                (cons -0.5 0.5)
                (cons -0.5 0.5))
)

#(define (ly:moment-abs moment)
  (let* (
    (num (ly:moment-main-numerator moment))
    (d (ly:moment-main-denominator moment))
    )
    (ly:make-moment (abs num) d)
  )
)

#(define (get-upper-staff-pos grob-a grob-b)
  (let*
    (
      (min-val (min (ly:grob-property grob-a 'staff-position) (ly:grob-property grob-b 'staff-position)))
    )
  (if (equal? min-val (ly:grob-property grob-a 'staff-position))
          grob-b
          grob-a
      )
))

#(define (get-lower-staff-pos grob-a grob-b)
  (let*
    (
      (min-val (min (ly:grob-property grob-a 'staff-position) (ly:grob-property grob-b 'staff-position)))
    )
  (if (equal? min-val (ly:grob-property grob-a 'staff-position))
          grob-a
          grob-b
      )
))

%!!find overlapping durations
#(define (find-duration-overlap new-note old-note)
  (let* (
    (old-grob (third old-note))
    (new-grob (third new-note))
    (notecol (ly:grob-parent old-grob X))
    (notecol-new (ly:grob-parent new-grob X))
    (noteheads (ly:grob-array->list (ly:grob-object notecol 'note-heads)))
    (meta-old (ly:grob-property notecol 'meta))
    (overlap (ly:moment-abs (ly:moment-sub (first new-note) (second old-note) )))
    )
  (if (ly:moment<? (ly:make-moment 0 0 0) overlap)
        ;;check if chord
        (if (eqv? notecol notecol-new)
              (begin
                ;;if chord set lower note green
                ;(ly:grob-set-property! (get-lower-staff-pos old-grob new-grob) 'color green)
                (ly:grob-set-property! (get-lower-staff-pos old-grob new-grob) 'meta
                        (append
                            (ly:grob-property (get-lower-staff-pos old-grob new-grob) 'meta)
                              (list (cons 'is-lower-in-chord #t))))
                ;(display "Chord")(newline)
              )
              ;;if not chord
              (begin
                ;(display "Not Chord")(newline)
                ;;if not a chord just make grob relation
                ;(ly:grob-set-property! old-grob 'color red)
                ;;set the meta value in notecolumn so that we can access it from chord-heads
                ;;first check back to see if this note is part of a chords
                (ly:grob-set-property! notecol 'meta
                            (append meta-old (list (cons 'other-grob new-grob))))
              )
        )
        (begin
            (display "Othering")(newline) ; needs to do something for no error
        )
    )
))

#(define (extract-timing context notehead)
  (let*
    (
      (start-point (ly:context-current-moment context))
      (duration (ly:event-property (ly:grob-property notehead 'cause) 'length))
      (end-point (ly:moment-add start-point duration))
    )
    ;;return a list of grob start and end point
   (list start-point end-point notehead)
  )
)

#(define (interrupt_heads_engraver ctx)
   (let (
      (noteheads '())
    )
    `(
      (acknowledgers
          (note-head-interface . , (lambda (trans grob source)
                (set! noteheads (cons (extract-timing ctx grob) noteheads)))
          )
        )
       (process-acknowledged
        . ,(lambda (trans)
            (begin
             (if (>= (length noteheads) 2)
                 (begin
                   ; (display noteheads)(newline)
                   (find-duration-overlap (first noteheads) (last noteheads))
                   (set! noteheads (list (first noteheads)))
                  )
                )
             ))
          )
      )
))

#(define (get-distance x y)
    (- (cdr y) (car x))
)

%!!music function -problem is with (ly:grob-extent grob sys Y))
interrupt = #(define-music-function (value) (number?)
  #{
      \override Staff.NoteHead.cross-staff = ##t
      \once \override Staff.NoteHead.after-line-breaking = #(lambda (grob)
              (let* (
                (stem (ly:grob-object grob 'stem))
                (stem-dir (ly:grob-property stem 'direction))
                (stem-thickness (ly:grob-property stem 'thickness))
                (thickness (/ stem-thickness 10))
                (notecol (ly:grob-parent grob X))
                (meta  (assoc 'other-grob (ly:grob-property notecol 'meta)))
                (other (if meta
                              (cdr meta)
                              grob
                      ))
                (notehead-width (cdr (ly:grob-property grob 'X-extent)))
                (sys (ly:grob-system grob))
                (now-pos (ly:grob-extent grob sys X))
                (next-pos (ly:grob-extent other sys X))

                ; does not work. skyline calculation unavailable
                ;(now-pos-y (ly:grob-extent grob sys Y)) ; greg
                ;(next-pos-y (ly:grob-extent other sys Y)) ; greg
                (x-distance
                    (if (= stem-dir -1)
                      (+ (- (get-distance now-pos next-pos) notehead-width ) (/ thickness 2))
                      (- (get-distance now-pos next-pos) (/ thickness 2))
                    ))
                ; does not work. skyline calculation unavailable
                ;(y-distance
                ;    (if (= stem-dir -1)
                ;      (+ (- (get-distance now-pos-y next-pos-y) notehead-width ) (/ thickness 2))
                ;      (- (get-distance now-pos-y next-pos-y) (/ thickness 2))
                ;    ))
                (ps-bracket
                    (if (= stem-dir -1)
                      (draw-ps-bracket x-distance notehead-width (- value 0.5) thickness)
                      (draw-ps-bracket x-distance notehead-width value thickness)
                    ))
                ; does not work. skyline calculation unavailable
                ;(ps-bracket
                ;    (if (= stem-dir -1)
                ;      (draw-ps-bracket x-distance notehead-width (- y-distance 0.5) thickness)
                ;      (draw-ps-bracket x-distance notehead-width y-distance thickness)
                ;    ))
                (ps-line (draw-ps-line x-distance notehead-width thickness))
                (grob-stencil (ly:grob-property grob 'stencil))
                (stencil-bracket (ly:stencil-add grob-stencil ps-bracket ))
                (stencil-line (ly:stencil-add grob-stencil ps-line))
                )
                (if (assoc 'is-lower-in-chord (ly:grob-property grob 'meta))
                        (ly:grob-set-property! grob 'stencil stencil-line)
                        (ly:grob-set-property! grob 'stencil stencil-bracket)
                  )
              )
            )
  #}
)


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
