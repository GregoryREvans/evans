\version "2.23.14" % temp
xyOut =
#(define-music-function (parser location y-length)(number?)
  #{
     \once \override  Stem #'stencil =
       #(lambda (grob)
          (ly:grob-set-property! grob 'stem-end-position $y-length)
          (ly:stem::print grob))
  #})

#(define ((grow-beam-var number integer-beams) grob)
 (cond ((not (integer? integer-beams))
        (display "Use an integer value as second argument of grow-beam-var"))
   (else
 (cond
   ((< (length (cdr (ly:grob-property (ly:grob-parent grob X) 'beaming))) 2)
    (ly:beam::print grob))
   ((or (= number 0) (and (< number 0) (> (abs number)(1- (ly:grob-array-length (ly:grob-object grob 'stems))))))
    (begin
      (ly:grob-set-property! grob 'grow-direction LEFT)
      (ly:beam::print grob)))
   ((>= number (1- (ly:grob-array-length (ly:grob-object grob 'stems))))
    (begin
     (ly:grob-set-property! grob 'grow-direction RIGHT)
     (ly:beam::print grob)))

   ((ly:stencil? (ly:beam::print grob)) ;; delete this?
    (let* ((beam (ly:beam::print grob))
           (beam-positions (ly:grob-property grob 'positions))
           (beam-slant (cond ((<= (car beam-positions) (cdr beam-positions)) 1)
                             ;;((= (car beam-positions) (cdr beam-positions)) 0)
                             ((> (car beam-positions) (cdr beam-positions)) -1)))
           (dir (ly:beam::calc-direction grob))
           (b-d (ly:output-def-lookup (ly:grob-layout grob) 'blot-diameter))
           (beam-extent-X (ly:stencil-extent beam X))
           (beam-length-x-orig (interval-length beam-extent-X))
           (beam-length-x (- beam-length-x-orig b-d))
           (beam-extent-Y (ly:stencil-extent beam Y))
           (beam-length-y (interval-length beam-extent-Y))
           (orig-beam-thickness (ly:grob-property grob 'beam-thickness))
           (beam-count (length (cdr (ly:grob-property (ly:grob-parent grob X) 'beaming))))
           ;(beam-count (if (= 2 integer-beams)
           ;	             (- orig-beam-count 1)
           ;	             orig-beam-count))
           (space-between-beams (* 0.46 (ly:grob-property grob 'gap)))
           (orig-beam-length-at-stem (+ (* beam-count orig-beam-thickness)(* (- beam-count 1) space-between-beams)))
           (orig-slope (* beam-slant (/ (- beam-length-y orig-beam-length-at-stem) beam-length-x)))
           (alpha (atan orig-slope))
           (beam-thickness (* 0.8 orig-beam-thickness))
           (h-max (- (/ orig-beam-length-at-stem (cos alpha)) (* 1.3 beam-thickness)))
           (number-a (if (integer? (abs number))
                   (abs number)
                   (inexact->exact (truncate (abs number)))))
           (number-b (- (abs number) (truncate (abs number))))
           (stems (ly:grob-object grob 'stems))
           (stem-count (ly:grob-array-length stems))
           (refp (ly:grob-system grob))
           (first-stem (ly:grob-array-ref stems 0))
           (first-stem-dir (ly:grob-property first-stem 'direction))
           (last-stem (ly:grob-array-ref stems (- stem-count 1)))
           (last-stem-dir (ly:grob-property last-stem 'direction))
           (target-stem (if (< (abs number-a) stem-count)
                   (ly:grob-array-ref stems number-a)
                   (ly:grob-array-ref stems (- stem-count 1 ))))
           (next-stem (if (< (+ (abs number-a) 1) stem-count)
                   (ly:grob-array-ref stems (+ number-a 1))
                   (ly:grob-array-ref stems (- stem-count 1 ))))
           (first-stem-coord (ly:grob-relative-coordinate first-stem refp X))
           (target-stem-coord (ly:grob-relative-coordinate target-stem refp X))
           (next-stem-coord (ly:grob-relative-coordinate next-stem refp X))
           (first-stem-to-target-stem-length (interval-length (cons first-stem-coord target-stem-coord)))
           (stem-to-next-stem-length (interval-length (cons target-stem-coord next-stem-coord)))
           (factor (/ beam-length-x (+ first-stem-to-target-stem-length (* number-b stem-to-next-stem-length))))
           (y-sp (lambda (n) (* -1 n dir (+ beam-thickness space-between-beams))))
           (y-off (* 1 (/ (- beam-length-y orig-beam-length-at-stem) factor)))


;; markup-a is the longest beam

           (markup-a (markup #:beam beam-length-x
                                    orig-slope
                                    beam-thickness))

  ;; left piece
     ;; y-length of left piece
           (y-L
             (lambda (n)
               (if (>= number 0)
                 (- (/ (- beam-length-y orig-beam-length-at-stem) factor) (* dir beam-slant n (/ h-max (- beam-count 1))))
                 (+ (/ (- beam-length-y orig-beam-length-at-stem) factor) (* dir beam-slant n (+ beam-thickness space-between-beams)))
                 )))
     ;; x-length of left piece
           (x-L (+ first-stem-to-target-stem-length (* number-b stem-to-next-stem-length)))
     ;; slope of left piece
           (slope-part-beam-L
             (lambda (n)
               (if (>= number 0)
                   (cond ((or (and (> dir 0) (> beam-slant 0)) (and (< dir 0) (> beam-slant 0)))
                          (/ (y-L n) x-L))
                         ((or (and (> dir 0) (< beam-slant 0)) (and (< dir 0) (< beam-slant 0)))
                          (* -1 (/ (y-L n) x-L))))
                   (cond ((or (and (> dir 0) (> beam-slant 0))(and (< dir 0) (> beam-slant 0)))
                          (/ (y-L n) x-L))
                         ((or (and (> dir 0) (< beam-slant 0))(and (< dir 0) (< beam-slant 0)))
                          (* -1 (/ (y-L n) x-L))))
                      )))
     ;; construct left piece
           (part-beam-L
             (lambda (n)
                 (markup #:beam x-L
                                (slope-part-beam-L n)
                                beam-thickness)))
     ;; markup of left piece
           (markup-L (lambda (n) (markup (part-beam-L n))))
     ;; stencil of left piece
           (beam-part-L (lambda (n) (grob-interpret-markup grob (markup-L n))))
     ;; y-extent of left piece
           (beam-part-L-ext-y (lambda (n) (ly:stencil-extent (beam-part-L n) Y)))
     ;; length of left piece
           (length-beam-part-L-y (lambda (n) (interval-length (beam-part-L-ext-y n))))

  ;; right piece
           (y-R (lambda (n) (- (- beam-length-y orig-beam-length-at-stem) (y-L n))))
           (x-R (- beam-length-x x-L))
           (slope-part-beam-R
             (lambda (n)
               (cond
                     ((or (and (> dir 0) (> beam-slant 0)) (and (< dir 0) (> beam-slant 0)))
                      (/ (y-R n) x-R))
                     ((or (and (> dir 0) (< beam-slant 0)) (and (< dir 0) (< beam-slant 0)))
                      (* -1  (/ (y-R n) x-R))))))
           (part-beam-R
             (lambda (n)
               (markup #:beam (- beam-length-x x-L)
                              (slope-part-beam-R n)
                              beam-thickness)))
           (markup-R (lambda (n) (markup (part-beam-R n))))

   ;; parts of feathered beams
           (beam-pieces
             (map
               (lambda (n)
                 (ly:stencil-combine-at-edge
                   (ly:stencil-translate-axis
                     (ly:stencil-translate-axis
                       (grob-interpret-markup grob (markup-L n))
                       -0.025 X)
                   (if (>= number 0)
                       0
                       (y-sp n))
                   Y)
                   X RIGHT
                   (ly:stencil-translate-axis
                     (grob-interpret-markup grob (markup-R n))
                     (if (>= number 0)
                        (cond ((and (> dir 0)(> beam-slant 0))
                               (if (and (>= (slope-part-beam-L n) 0)(>= (slope-part-beam-R n) 0))
                                   (- (length-beam-part-L-y n) beam-thickness)
                                   (* -1 (- (length-beam-part-L-y n) beam-thickness))))
                              ((and (> dir 0)(< beam-slant 0))
                               (* -1 (- (length-beam-part-L-y n) beam-thickness)))

                              ((and (< dir 0)(> beam-slant 0))
                               (- (length-beam-part-L-y n) beam-thickness))
                              ((and (< dir 0)(< beam-slant 0))
                               (if (and (<= (slope-part-beam-L n) 0)(<= (slope-part-beam-R n) 0))
                                   (* -1 (- (length-beam-part-L-y n) beam-thickness))
                                   (- (length-beam-part-L-y n) beam-thickness)))
                              )
                        (cond ((or (and (> dir 0)(> beam-slant 0))(and (< dir 0)(> beam-slant 0)))
                               y-off)
                              ((or (and (> dir 0)(< beam-slant 0))(and (< dir 0)(< beam-slant 0)))
                               (* -1 y-off))
                               )
                           )
                     Y)
                   0))
                   (if (= integer-beams 2)
                     (iota (- beam-count 1))
                     (cdr (iota (- beam-count 0))))
               ))

                       )   ;; end of defs in let*



      (define (helper beam-pieces)
        (ly:stencil-add
          (car beam-pieces)
          (if (null? (cdr beam-pieces))
              (car beam-pieces)
              (helper (cdr beam-pieces)))))

      (ly:stencil-translate-axis
       (ly:stencil-add
         ;; first (long beam)
           (ly:stencil-translate
             (grob-interpret-markup grob markup-a)
               '(-0.025 . 0))
           (cond ((= integer-beams 2)
                    (ly:stencil-translate
                      (grob-interpret-markup grob markup-a)
                        (cons -0.025  (* (+ beam-thickness space-between-beams) -1 dir))))
                  (else (grob-interpret-markup grob "")))
           ;; other beams
           (ly:stencil-translate-axis
             (helper beam-pieces)
               (if (= integer-beams 2)
                 (* space-between-beams -2 dir)
                 0)
               Y)
       )

       (car beam-positions)
       ;;beam-thickness
       Y)
       ;(newline)(display beam-count)
     ) ;; end of let*
    )
  )
)
))

#(define (moment=? a b)
   (not (or (ly:moment<? a b) (ly:moment<? b a))))

#(define (moment>? a b)
   (not (or (ly:moment<? a b) (moment=? a b))))

featherDurationsTest=
#(define-music-function (parser location factor turnaround-orig argument)
                                         (ly:moment? number? ly:music?)
   (let* ((orig-duration (ly:music-length argument))
          (multiplier (ly:make-moment 1 1))
          (turnaround (if (and (integer? turnaround-orig) (>= turnaround-orig 0))
          		turnaround-orig
          		(inexact->exact (floor (abs turnaround-orig)))))
          (elements (ly:music-property argument 'elements))
          (dif (- (length elements) turnaround))
          (lth (cond ((>= dif 0) dif)
                     (else (length elements))))
          (peak-multiplier
            (reduce
              (lambda (mom prev) (ly:moment-mul mom prev))
              multiplier
              (make-list turnaround factor)))
          (end-multiplier
            (reduce
              (lambda (mom prev) (ly:moment-mul mom prev))
              peak-multiplier
              (append
                (list peak-multiplier)
                (make-list lth ;;(- (length elements) turnaround)
                           (ly:moment-div (ly:make-moment 1 1) factor)))))
          (comparison
            (if (< (ly:moment-main-numerator factor) (ly:moment-main-denominator factor))
                (lambda (a b) (ly:moment<? a b))
                (lambda (a b) (moment>? a b)))))
     (music-map
       (lambda (mus)
         (if (and (eq? (ly:music-property mus 'name) 'EventChord)
                  (< 0 (ly:moment-main-denominator (ly:music-length mus))))
             (begin
               ;;(display multiplier) (newline) ; shows pattern of modification
               (ly:music-compress mus multiplier)
               (if (comparison peak-multiplier multiplier)
                   (set! multiplier (ly:moment-mul factor multiplier))
                   (begin
                     (set! multiplier (ly:moment-div multiplier factor))
                     (set! peak-multiplier end-multiplier)))))
        mus)
      argument)

     (ly:music-compress
       argument
       (ly:moment-div orig-duration (ly:music-length argument)))

     argument))
