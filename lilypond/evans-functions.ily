%%% staff lines %%%

staff-line-count = #(
    define-music-function (parser location number music) (number? ly:music?)
    #{
    \stopStaff
    \override Staff.StaffSymbol.line-count = #number
    \startStaff
    $music
    #}
    )

%%% duration line style %%%

duration-line-style = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \omit Stem
    \once \omit Flag
    \once \omit Beam
    \once \omit Dots
    \once \override DurationLine.style = #'line
    \once \override NoteHead.duration-log = 2
    $music
    #}
    )

%%% flat ties %%%

#(define ((flared-tie coords) grob)

  (define (pair-to-list pair)
     (list (car pair) (cdr pair)))

  (define (normalize-coords goods x y dir)
    (map
      (lambda (coord)
        ;(coord-scale coord (cons x (* y dir)))
        (cons (* x (car coord)) (* y dir (cdr coord))))
      goods))

  (define (my-c-p-s points thick)
    (make-connected-path-stencil
      points
      thick
      1.0
      1.0
      #f
      #f))

  ;; outer let to trigger suicide
  (let ((sten (ly:tie::print grob)))
    (if (grob::is-live? grob)
        (let* ((layout (ly:grob-layout grob))
               (line-thickness (ly:output-def-lookup layout 'line-thickness))
               (thickness (ly:grob-property grob 'thickness 0.1))
               (used-thick (* line-thickness thickness))
               (dir (ly:grob-property grob 'direction))
               (xex (ly:stencil-extent sten X))
               (yex (ly:stencil-extent sten Y))
               (lenx (interval-length xex))
               (leny (interval-length yex))
               (xtrans (car xex))
               (ytrans (if (> dir 0)(car yex) (cdr yex)))
               (uplist
                 (map pair-to-list
                      (normalize-coords coords lenx (* leny 2) dir))))

   (ly:stencil-translate
       (my-c-p-s uplist used-thick)
     (cons xtrans ytrans)))
   '())))

#(define flare-tie
  (flared-tie '((0 . 0)(0.06 . 0.1) (0.94 . 0.1) (1.0 . 0.0))))


%%% oval bar numbers %%%

#(define-markup-command (oval layout props arg)
   (markup?)
   #:properties ((thickness 1)
                 (font-size 0)
                 (oval-padding 0.5))
   (let ((th (* (ly:output-def-lookup layout 'line-thickness)
                thickness))
         (pad (* (magstep font-size) oval-padding))
         (m (interpret-markup layout props (markup #:hcenter-in 4.0 arg))))
     (oval-stencil m th pad (* pad 8.0))))

#(define (oval-bar-numbers barnum measure-pos alt-number context)
   (make-oval-markup
    (robust-bar-number-function barnum measure-pos alt-number context)))


%%% cautionary accidentals %%%

overhead-accidentals = #(
    define-music-function
    (font-size)
    (number?)
    #{
    \set suggestAccidentals = ##t
    \override Voice.AccidentalSuggestion.font-size = #font-size
    \override Voice.AccidentalSuggestion.parenthesized = ##f
    #}
    )

normal-accidentals = #(
    define-music-function
    (font-size)
    (number?)
    #{
    \set suggestAccidentals = ##f
    \revert Voice.AccidentalSuggestion.font-size
    \revert Voice.AccidentalSuggestion.parenthesized
    #}
    )

%%% evans new spacing section %%%
evans-new-spacing-section = #(
    define-music-function
    (parser location n d music)
    (number? number? ly:music?)
    #{
    \set Score.proportionalNotationDuration = #(ly:make-moment n d)
    \newSpacingSection
    $music
    #}
    )

%%% bend before %%%
#(define (make-bend x)
    (make-music 'BendAfterEvent
    'delta-step x)
)

bend = #(
    define-music-function (parser location delta) (integer?)
    (
        make-bend (* -1 delta)
    )
)

bendBeforeNegative = #(
    define-music-function (parser location argument) (integer?)
    #{
        \once \override BendAfter #'rotation = #'(180 -1.8 -1)
        \bend #argument
    #}
)

bendBeforePositive = #(
    define-music-function (parser location argument) (integer?)
    #{
        \once \override BendAfter #'rotation = #'(180 -1.8 1)
        \bend #argument
    #}
)

#(define-markup-command
    (ekmelos-char layout props point-code)
    (number?)
    (interpret-markup layout props
    #{
    \markup
    \fontsize #7
    \override #'(font-name . "ekmelos")
    \char #point-code
    #}))


%%% STEMS %%%

%%% sprechstimme %%%
speakOn = {
  \override Stem.stencil =
    #(lambda (grob)
       (let* ((x-parent (ly:grob-parent grob X))
              (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
         (if is-rest?
             empty-stencil
             (ly:stencil-combine-at-edge
              (ly:stem::print grob)
              Y
              (- (ly:grob-property grob 'direction))
              (grob-interpret-markup grob
                                     (markup #:center-align #:fontsize -4
                                             #:musicglyph "noteheads.s2cross"))
              -1.75))))
}
% above was -2.3 now -1.75
speakOff = {
  \revert Stem.stencil
  \revert Flag.stencil
}

%%% triangle stem %%%
triangleStemOn = {
  \override Stem.stencil =
    #(lambda (grob)
       (let* ((x-parent (ly:grob-parent grob X))
              (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
         (if is-rest?
             empty-stencil
             (ly:stencil-combine-at-edge
              (ly:stem::print grob)
              Y
              (- (ly:grob-property grob 'direction))
              (grob-interpret-markup grob
                                     (markup #:center-align #:fontsize -2
                                             #:musicglyph "arrowheads.close.1M1"))
              -1.75))))
}

%%% z stem %%%
zStemOn = {
  \override Stem.stencil =
    #(lambda (grob)
       (let* ((x-parent (ly:grob-parent grob X))
              (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
         (if is-rest?
             empty-stencil
             (ly:stencil-combine-at-edge
              (ly:stem::print grob)
              Y
              (- (ly:grob-property grob 'direction))
              (grob-interpret-markup grob
                                     (markup #:center-align #:fontsize -1.5 #:bold
                                             "z"))
              -1.75))))
}
% above was -2.3 now -1.75

%%% irregular tremolo stem %%%
irregularStemOn = {
  \override Stem.stencil =
    #(lambda (grob)
       (let* ((x-parent (ly:grob-parent grob X))
              (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
         (if is-rest?
             empty-stencil
             (ly:stencil-combine-at-edge
              (ly:stem::print grob)
              Y
              (- (ly:grob-property grob 'direction))
              (grob-interpret-markup grob
                                     (markup #:center-align #:hspace 0.01 #:fontsize -6.5 #:ekmelos-char #xe22c))
              -2.5))))
}

%%% z stem %%%
zStemOn = {
  \override Stem.stencil =
    #(lambda (grob)
       (let* ((x-parent (ly:grob-parent grob X))
              (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
         (if is-rest?
             empty-stencil
             (ly:stencil-combine-at-edge
              (ly:stem::print grob)
              Y
              (- (ly:grob-property grob 'direction))
              (grob-interpret-markup grob
                                     (markup #:center-align #:hspace 0.01 #:fontsize -6.5 #:ekmelos-char #xe22b))
              -1.75))))
}

stemOff = {
  \revert Stem.stencil
  \revert Flag.stencil
}

%%% NOTE HEAD PATTERNS %%%
squared = {
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (<= dur 1)
                    (grob-interpret-markup grob (markup #:musicglyph "noteheads.s0la"))
                    (if (> dur 1)
                        (grob-interpret-markup grob (markup #:musicglyph "noteheads.s2la"))
                    )
                )
            )
        )
}

slapped = {
    \override NoteHead.stem-attachment = #'(1 . -0.125)
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (<= dur 1)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xec5a))
                    (if (> dur 1)
                        (grob-interpret-markup grob (markup #:musicglyph "scripts.sforzato"))
                    )
                )
            )
        )
}

half-harmonic = {
    \override NoteHead.stem-attachment = #'(0 . 0.5) % different x for up vs down?
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (<= dur 1)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe0fc))
                    (if (> dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xe0e3))
                    )
                )
            )
        )
}

slashed-dot = {
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (> dur 1)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe0cf))
                    (if (= dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xe0d1))
                        (if (= dur 0)
                            (grob-interpret-markup grob (markup #:ekmelos-char #xe0d3))
                        )
                    )
                )
            )
        )
}

kiss-on = {
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (> dur 1)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe1c5 #:hspace -0.75 #:ekmelos-char #xe0a4))
                    (if (= dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xe1c5 #:hspace -0.75 #:ekmelos-char #xe0a3))
                        (if (= dur 0)
                            (grob-interpret-markup grob (markup #:ekmelos-char #xe1c5 #:hspace -0.75 #:ekmelos-char #xe0a2))
                        )
                    )
                )
            )
        )
}

kiss-off = {
    \override NoteHead.stem-attachment = #'(0 . 0)
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (> dur 1)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe0a4 #:hspace -0.75 #:ekmelos-char #xe1c5))
                    (if (= dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xe0a3 #:hspace -0.75 #:ekmelos-char #xe1c5))
                        (if (= dur 0)
                            (grob-interpret-markup grob (markup #:ekmelos-char #xe0a2 #:hspace -0.75 #:ekmelos-char #xe1c5 ))
                        )
                    )
                )
            )
        )
}

air-tone = {
    \override NoteHead.stem-attachment = #'(0 . -1.5)
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (<= dur 1)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe114))
                    (if (> dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xe113))
                    )
                )
            )
        )
    \override Staff.AccidentalPlacement.right-padding = #0.6
}

half-air-tone = {
    \override NoteHead.stem-attachment = #'(0 . -1.5)
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (<= dur 1)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe115))
                    (if (> dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xf67e))
                    )
                )
            )
        )
    \override Staff.AccidentalPlacement.right-padding = #0.6
}

highest = {
    \override NoteHead.stem-attachment = #'(0 . 0.75)
    \override NoteHead.no-ledgers = ##t
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (= dur 0)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe0bb))
                    (if (= dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xe0bc))
                        (if (> dur 1)
                            (grob-interpret-markup grob (markup #:ekmelos-char #xe0be))
                        )
                    )
                )
            )
        )
    \override Staff.AccidentalPlacement.right-padding = #0.6
}

lowest = {
    \override NoteHead.stem-attachment = #'(0 . 0.75)
    \override NoteHead.no-ledgers = ##t
    \override NoteHead.stencil =
        #(lambda (grob)
            (let ((dur (ly:grob-property grob 'duration-log)))
                (if (= dur 0)
                    (grob-interpret-markup grob (markup #:ekmelos-char #xe0c4))
                    (if (= dur 1)
                        (grob-interpret-markup grob (markup #:ekmelos-char #xe0c5))
                        (if (> dur 1)
                            (grob-interpret-markup grob (markup #:ekmelos-char #xe0c7))
                        )
                    )
                )
            )
        )
    \override Staff.AccidentalPlacement.right-padding = #0.6
}

revert-noteheads = {
  \revert NoteHead.stem-attachment
  \revert NoteHead.stencil
  \revert Staff.AccidentalPlacement.right-padding
  \override NoteHead.no-ledgers = ##f
}

%%% CLEFS %%%
fingerboard-clef = {
    \override Staff.Clef.stencil =
        #(lambda (grob)
            (grob-interpret-markup grob (markup #:fontsize -5.5 #:raise 1 #:ekmelos-char #xe078))
        )
}

%%% custom vibrato %%%

%{ \version "2.23.14" %}

%% https://raw.githubusercontent.com/mwitmer/LyUtil/master/ly/expressive_markings/vibrato.ly
%% Original author: Mark Witmer
%% Rewritten version by Harm

#(define (line-part-min-max x1 x2)
  (list (min x1 x2) (max x1 x2)))

#(define (bezier-part-min-max x1 x2 x3 x4)
  ((lambda (x) (list (reduce min 10000 x) (reduce max -10000 x)))
   (map
    (lambda (x)
      (+ (* x1 (expt (- 1 x) 3))
         (+ (* 3 (* x2 (* (expt (- 1 x) 2) x)))
            (+ (* 3 (* x3 (* (- 1 x) (expt x 2))))
               (* x4 (expt x 3))))))
    (if (< (+ (expt x2 2) (+ (expt x3 2) (* x1 x4)))
           (+ (* x1 x3) (+ (* x2 x4) (* x2 x3))))
        (list 0.0 1.0)
        (filter
         (lambda (x) (and (>= x 0) (<= x 1)))
         (append
          (list 0.0 1.0)
          (map (lambda (op)
                 (if (not (eqv? 0.0
                                (exact->inexact (- (+ x1 (* 3 x3)) (+ x4 (* 3 x2))))))
                     ;; Zeros of the bezier curve
                     (/ (+ (- x1 (* 2 x2))
                           (op x3
                               (sqrt (- (+ (expt x2 2)
                                           (+ (expt x3 2) (* x1 x4)))
                                        (+ (* x1 x3)
                                           (+ (* x2 x4) (* x2 x3)))))))
                        (- (+ x1 (* 3 x3)) (+ x4 (* 3 x2))))
                     ;; Apply L'hopital's rule to get the zeros if 0/0
                     (* (op 0 1)
                        (/ (/ (- x4 x3) 2)
                           (sqrt (- (+ (* x2 x2)
                                       (+ (* x3 x3) (* x1 x4)))
                                    (+ (* x1 x3)
                                       (+ (* x2 x4) (* x2 x3)))))))))
               (list + -))))))))

#(define (bezier-min-max x1 y1 x2 y2 x3 y3 x4 y4)
  (map (lambda (x)
         (apply bezier-part-min-max x))
       `((,x1 ,x2 ,x3 ,x4) (,y1 ,y2 ,y3 ,y4))))

#(define (line-min-max x1 y1 x2 y2)
  (map (lambda (x)
         (apply line-part-min-max x))
       `((,x1 ,x2) (,y1 ,y2))))

#(define (path-min-max origin pointlist)

  ((lambda (x)
     (list
      (reduce min +inf.0 (map caar x))
      (reduce max -inf.0 (map cadar x))
      (reduce min +inf.0 (map caadr x))
      (reduce max -inf.0 (map cadadr x))))
   (map (lambda (x)
          (if (= (length x) 8)
              (apply bezier-min-max x)
              (apply line-min-max x)))
        (map (lambda (x y)
               (append (list (cadr (reverse x)) (car (reverse x))) y))
             (append (list origin)
                     (reverse (cdr (reverse pointlist)))) pointlist))))

#(define (make-path-stencil path thickness x-scale y-scale fill)
  "Make a stencil based on the path described by the list @var{path},
with thickness @var{thickness}, and scaled by @var{x-scale} in the X
direction and @var{y-scale} in the Y direction.  @var{fill} is a boolean
argument that specifies if the path should be filled.  Valid path
commands are: moveto rmoveto lineto rlineto curveto rcurveto closepath,
and their standard SVG single letter equivalents: M m L l C c Z z."

  (define (convert-path path origin previous-point)
    "Recursive function to standardize command names and
convert any relative path expressions (in @var{path}) to absolute
values.  Returns a list of lists.  @var{origin} is a pair of x and y
coordinates for the origin point of the path (used for closepath and
reset by moveto commands).  @var{previous-point} is a pair of x and y
coordinates for the previous point in the path."
    (if (pair? path)
        (let*
         ((head-raw (car path))
          (rest (cdr path))
          (head (cond
                 ((memq head-raw '(rmoveto M m)) 'moveto)
                 ((memq head-raw '(rlineto L l)) 'lineto)
                 ((memq head-raw '(rcurveto C c)) 'curveto)
                 ((memq head-raw '(Z z)) 'closepath)
                 (else head-raw)))
          (arity (cond
                  ((memq head '(lineto moveto)) 2)
                  ((eq? head 'curveto) 6)
                  (else 0)))
          (coordinates-raw (take rest arity))
          (is-absolute (if (memq head-raw
                           '(rmoveto m rlineto l rcurveto c)) #f #t))
          (coordinates (if is-absolute
                           coordinates-raw
                           ;; convert relative coordinates to absolute by
                           ;; adding them to previous point values
                           (map (lambda (c n)
                                  (if (even? n)
                                      (+ c (car previous-point))
                                      (+ c (cdr previous-point))))
                             coordinates-raw
                             (iota arity))))
          (new-point (if (eq? head 'closepath)
                         origin
                         (cons
                          (list-ref coordinates (- arity 2))
                          (list-ref coordinates (- arity 1)))))
          (new-origin (if (eq? head 'moveto)
                          new-point
                          origin)))
         (cons (cons head coordinates)
           (convert-path (drop rest arity) new-origin new-point)))
        '()))

  (let* ((path-absolute (convert-path path (cons 0 0) (cons 0 0)))
         ;; scale coordinates
         (path-scaled (if (and (= 1 x-scale) (= 1 y-scale))
                          path-absolute
                          (map (lambda (path-unit)
                                 (map (lambda (c n)
                                        (cond
                                         ((= 0 n) c)
                                         ((odd? n) (* c x-scale))
                                         (else (* c y-scale))))
                                   path-unit
                                   (iota (length path-unit))))
                            path-absolute)))
         ;; a path must begin with a 'moveto'
         (path-final (if (eq? 'moveto (car (car path-scaled)))
                         path-scaled
                         (append (list (list 'moveto 0 0)) path-scaled)))
         ;; remove all commands in order to calculate bounds
         (path-headless (map cdr (delete (list 'closepath) path-final)))
         (bound-list (path-min-max
                      (car path-headless)
                      (cdr path-headless))))
    (ly:make-stencil
     `(path ,thickness
        ,(concatenate path-final)
        round
        round
        ,(if fill #t #f))
     (coord-translate
      ((if (< x-scale 0) reverse-interval identity)
       (cons
        (list-ref bound-list 0)
        (list-ref bound-list 1)))
      `(,(/ thickness -2) . ,(/ thickness 2)))
     (coord-translate
      ((if (< y-scale 0) reverse-interval identity)
       (cons
        (list-ref bound-list 2)
        (list-ref bound-list 3)))
      `(,(/ thickness -2) . ,(/ thickness 2))))))
% Returns the width of a grob
#(define (grob-width grob)
  (let ((x-ext (ly:grob-property grob 'X-extent)))
    (if (interval-sane? x-ext)
        (- (cdr x-ext) (car x-ext))
        0)))

#(define (apply-proc-to-leading-two-args proc ls rl)
  (if (null? (cdr ls))
      (reverse rl)
      (apply-proc-to-leading-two-args
        proc
        (cdr ls)
        (cons (proc (car ls) (cadr ls)) rl))))

#(define (make-amplitudes-list amplitudes total-span wavelength)
;;(format #t "\n\nMakes a list of amplitudes for the vibrato ~A ~A \n\n"  amplitudes (length amplitudes)) ;; prints results
  (if (= (length amplitudes) 1)
      (set! amplitudes (append amplitudes amplitudes)))
  (let* (
         ;; how many waves for the entire total-span
         (lngth (/ total-span wavelength))
         ;; the total-span is divided into parts:
         (parts (1- (length amplitudes)))
         ;; each part gets that much waves
         (partial-length (/ lngth parts))
         ;; get a list of amplitude-pairs, i.e.:
         ;; '(1 2 3 4) -> '((1 . 2) (2 . 3) (3 . 4))
         (amp-pairs
           (apply-proc-to-leading-two-args
             cons
             amplitudes
             '()))
         ;; calculate the amplitudes
         (amplitudes-list
           (append-map
             (lambda (amp-pair)
               (map
                 (lambda (n)
                   (+ (car amp-pair)
                       (* (/ n partial-length)
                          (- (cdr amp-pair) (car amp-pair)))))
                 (iota (ceiling partial-length))))
              amp-pairs)))
      ;; don't forget last amplitude
      (append amplitudes-list (list (last amplitudes)))))

#(define (wave-line-stencil left-bound x-span thick amplitude-list wave-length)

  (if (zero? x-span)
      empty-stencil
      (let* (;; get the amount of waves which will be needed
             (waves-amount (length amplitude-list))
             ;; the added waves would result in a line with length
             (raw-line-length (* waves-amount wave-length))
             ;; get the factor to scale the provided wave-length to ensure
             ;; matching lengths
             (corr (/ raw-line-length x-span))
             ;; calculate the scaled wave-length
             (scaled-wave-length (/ wave-length corr)))
         (make-path-stencil
           (append
             `(moveto ,left-bound 0.0)
             (append-map
               (lambda (amp)
                 `(rcurveto
                   ,(/ scaled-wave-length 3.0) ,amp
                   ,(* 2 (/ scaled-wave-length 3.0)) ,(- amp)
                   ,scaled-wave-length 0.0))
               amplitude-list))
            thick
            1
            1
            #f))))

#(define (make-wavy-vibrato-stencil grob amplitudes wave-length thickness)
"Creates a stencil that draws a wavy line for vibrato based on @var{amplitudes},
a list of vertival lengths, and @var{wave-length} for the horizontal extent.
"
  (let* ((orig (ly:grob-original grob))
         (siblings (if (ly:grob? orig) (ly:spanner-broken-into orig) '()))
         (thick (ly:grob-property grob 'thickness thickness ;;0.2
         ))
         ;; length of the actual grob
         (xspan (grob-width grob))
         ;; add the length of all siblings
         (total-span
           (if (null? siblings)
               (grob-width grob)
               (reduce + 0 (map (lambda (g) (grob-width g)) siblings))))
         ;; get the x-position for the start
         (left-bound
           (if (or (null? siblings) (eq? (car siblings) grob))
               ;; compensate thickness of the line
               (* thick -2)
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
         ;; get the entire list of amplitudes
         (amplitude-list
           (make-amplitudes-list amplitudes total-span wave-length))
         ;;;; limit the amplitude-list to the needed values
         ;;;; there may be rounding issues
         ;; delete already done amplitudes from 'amplitude-list'-head
         (amplitude-list-tail
            (drop
              amplitude-list
              (inexact->exact (floor (/ span-so-far wave-length)))))
         ;; limit 'amplitude-list-tail' to the actual needed values
         (amplitude-todo
           (if (zero? (inexact->exact (floor (/ xspan wave-length))))
               amplitude-list-tail
               (take
                 amplitude-list-tail
                 (inexact->exact (ceiling (/ xspan wave-length))))))
         ;; process the final stencil
         (final-stencil
           (wave-line-stencil
             left-bound
             xspan
             thick
             (if (null? siblings)
                 amplitude-list
                 amplitude-todo)
             wave-length))
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

vibrato =
#(define-music-function (amplitudes wave-length thickness) (list? number? number?)
"Overrides @code{TrillSpanner.after-line-breaking}, setting a new stencil,
drawning a wavy line looking at @var{amplitudes} and @var{wave-length} with thickness @var{thickness}.
Limitations:
  - @var{wave-length} is a constant, it can't be changed dynamically while
    processing one vibrato.
  - Each part of the vibrato (growing or shrinking) is of equal length.
    Would be nice to have something like:
      go from amplitude 1 to 4 while the underlying music lasts a quarter
"
#{
  \once \override TrillSpanner.after-line-breaking =
    #(lambda (grob)
       (ly:grob-set-property! grob 'stencil
         (make-wavy-vibrato-stencil grob amplitudes wave-length thickness)))
#})

vibratoGlissando =
#(define-music-function (amplitudes wave-length thickness) (list? number? number?)
"Overrides @code{TrillSpanner.after-line-breaking}, setting a new stencil,
drawning a wavy line looking at @var{amplitudes} and @var{wave-length} with thickness @var{thickness}.
Limitations:
  - @var{wave-length} is a constant, it can't be changed dynamically while
    processing one vibrato.
  - Each part of the vibrato (growing or shrinking) is of equal length.
    Would be nice to have something like:
      go from amplitude 1 to 4 while the underlying music lasts a quarter
"
#{
  \once \override Glissando.stencil =
    #(lambda (grob)
       (ly:grob-set-property! grob 'stencil
         (make-wavy-vibrato-stencil grob amplitudes wave-length thickness)))
#})




%{ #(use-modules (ice-9 match))

#(set-object-property! 'curvature-factor 'backend-type? number?)

vibrato =
#(define-music-function (amplitudes wave-length) (list? number?)
    #{
    \once \override TrillSpanner.normalized-endpoints = #ly:spanner::calc-normalized-endpoints
    \once \override TrillSpanner.curvature-factor = 0.35
    \once \override TrillSpanner.stencil =
        #(let* ((n-amplitudes-1 (1- (length amplitudes))))
            (grob-transformer 'stencil (lambda (grob original)
                (if (ly:stencil? original)
                    (match-let* (
                        ((left . right) (ly:grob-property grob 'normalized-endpoints))
                        (left-idx (inexact->exact (round (* n-amplitudes-1 left))))
                        (right-idx (inexact->exact (round (* n-amplitudes-1 right))))
                        (sublist (match (drop (take amplitudes (1+ right-idx)) left-idx) ((one) (list one one)) (lst lst)))
                        (original-ext (ly:stencil-extent original X))
                        (len (interval-length original-ext))
                        ((start . end) original-ext)
                        (position-increment (/ len (1- (length sublist))))
                        (thickness (* (ly:grob-property grob 'thickness 1.0) (ly:staff-symbol-line-thickness grob)))
                        (factor (ly:grob-property grob 'curvature-factor))
                        )
                    (make-path-stencil (append `(moveto ,start 0.0)
                        (let loop (
                            (position start)
                            (tail sublist)
                            (last-exact start)
                            (current-sign 1)
                            (acc '())
                            )
                        (if (>= position end)
                            (reverse! acc)
                            (match-let* (
                                (next-position (+ position wave-length))
                                (intermediate1 (+ position (* wave-length factor)))
                                (intermediate2 (+ position (* wave-length (- 1 factor))))
                                (from-last (- position last-exact))
                                ((previous-height next-height . _) tail)
                                (height
                                    (* current-sign
                                        (interval-index (cons previous-height next-height) (+ -1 (* 2 (/ from-last position-increment))))
                                    )
                                )
                                (path-component `(curveto ,intermediate1 ,height,intermediate2 ,height,next-position 0.0))
                                (new-acc (append-reverse path-component acc))
                            )
                            (if (>= from-last position-increment)
                                (loop next-position
                                    (cdr tail)
                                    (+ last-exact position-increment)
                                    (- current-sign)
                                    new-acc
                                )
                                (loop next-position
                                    tail
                                    last-exact
                                    (- current-sign)
                                    new-acc
                                )
                            )
                            )
                        )
                        )
                    )
                    thickness 1 1 #f)) '()
                )
            )
            )
        )
    #}) %}


%%% parenthesize all %%%
parentheAll = #(define-music-function (note) (ly:music?)
#{
  \once \override Parentheses.font-size = #-1
  \once \override Parentheses.stencil = #(lambda (grob)
       (let* ((acc (ly:grob-object (ly:grob-parent grob Y) 'accidental-grob))
              (dot (ly:grob-object (ly:grob-parent grob Y) 'dot)))
         (if (not (null? acc)) (ly:pointer-group-interface::add-grob grob 'elements acc))
         (if (not (null? dot)) (ly:pointer-group-interface::add-grob grob 'elements dot))
         (parentheses-interface::print grob)))
  \parenthesize $note
#})


%%% String Contact Point Spanner %%%


#(define (line-stencil left-bound x-span thick amplitude-list wave-height start-height)

  (if (zero? x-span)
      empty-stencil
      (let* (
             (waves-amount (length amplitude-list))
             ;; think about calculating amplitude heights relative to the width of the bars?
             ;;(max-amp (apply max amplitude-list))
             ;;(min-amp (apply min amplitude-list))
             ;;(interval (- max-amp min-amp))
             ;;(multiplier (/ (* 2 wave-height) interval))
             (step-size (/ x-span waves-amount))
             )
         (make-path-stencil
           (append
               `(moveto ,left-bound ,wave-height)
               `(lineto
                 ,x-span ,wave-height
                )
                `(moveto ,left-bound ,(- 0 wave-height))
                `(lineto
                  ,x-span ,(- 0 wave-height)
                 )
             `(moveto ,left-bound ,start-height)
             (append-map
               (lambda (amp)
                 `(rlineto
                   ,step-size ,amp
                  )
                 )
               amplitude-list))
            thick
            1
            1
            #f))))


#(define (make-scp-stencil grob amplitudes start-height wave-length thickness)
"Creates a stencil that draws a wavy line for vibrato based on @var{amplitudes},
a list of vertival lengths, and @var{wave-length} for the horizontal extent.
"
  (let* ((orig (ly:grob-original grob))
         (siblings (if (ly:grob? orig) (ly:spanner-broken-into orig) '()))
         (thick (ly:grob-property grob 'thickness thickness ;;0.2
         ))
         ;; length of the actual grob
         (xspan (grob-width grob))
         ;; add the length of all siblings
         (total-span
           (if (null? siblings)
               (grob-width grob)
               (reduce + 0 (map (lambda (g) (grob-width g)) siblings))))
         ;; get the x-position for the start
         (left-bound
           (if (or (null? siblings) (eq? (car siblings) grob))
               ;; compensate thickness of the line
               (* thick -2)
               ;; start a little left
               (1- (assoc-get 'X (ly:grob-property grob 'left-bound-info)))))
         (final-stencil
           (line-stencil
             left-bound
             xspan
             thick
             amplitudes
             wave-length
             start-height
             ))
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

string-contact-points =
#(define-music-function (amplitudes start-height wave-length thickness) (list? number? number? number?)
"Overrides @code{TrillSpanner.after-line-breaking}, setting a new stencil,
drawning a wavy line looking at @var{amplitudes} and @var{wave-length} with thickness @var{thickness}.
Limitations:
  - @var{wave-length} is a constant, it can't be changed dynamically while
    processing one vibrato.
  - Each part of the vibrato (growing or shrinking) is of equal length.
    Would be nice to have something like:
      go from amplitude 1 to 4 while the underlying music lasts a quarter
"
#{
  \once \override TextSpanner.after-line-breaking =
    #(lambda (grob)
       (ly:grob-set-property! grob 'stencil
         (make-scp-stencil grob amplitudes start-height wave-length thickness)))
#})
