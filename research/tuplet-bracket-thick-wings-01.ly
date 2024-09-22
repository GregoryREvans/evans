\version "2.24.3"

#(define (lists-map function ls)
  "Apply @var{function} to @var{ls} and all of it sublists.
First it recurses over the children, then the function is applied to
@var{ls}."
    (if (list? ls)
        (set! ls (map (lambda (y) (lists-map function y)) ls))
        ls)
    (function ls))

#(define (tuplet-bracket::line-parts grob stencil)
  "Examine @code{TupletBracket.stencil), accumulate lines used to draw
@code{TupletBracket}, divided into wings and horizontal lines."
  (if (ly:stencil-empty? stencil)
      '()
      (let* ((lines '())
             (edge-height (ly:grob-property grob 'edge-height))
             (stil-expr (ly:stencil-expr stencil))
             (staff-space (ly:staff-symbol-staff-space grob)))

        ;; accumulate the bracket-drawing lines in `lines`
        (when (pair? stil-expr)
          (lists-map
            (lambda (l)
              (when (and (list? l)
                         (eq? (list-ref l 0) 'draw-line)
                         ;; Broken TupletBracket may have collapsed wings,
                         ;; don't catch them. Deal with them when this procedure
                         ;; is called.
                         (not (zero?
                                (- (- (list-ref l 2) (list-ref l 4))
                                   (- (list-ref l 3) (list-ref l 5))))))
                (set! lines (cons l lines)))
              l)
            stil-expr))

        (call-with-values
          (lambda ()
            (partition
              (lambda (l)
                (let ((height (- (list-ref l 3) (list-ref l 5))))
                  ;; TODO looking at height is probably not safe enough.
                  ;; Avoid rounding issues
                  (or
                     (> 0.0000001
                        (abs (- (abs height)
                                (* staff-space (abs (car edge-height))))))
                     (> 0.0000001
                        (abs (- (abs height)
                                (* staff-space (abs (cdr edge-height)))))))))
              lines))
          (lambda (x y)
            (list (cons 'wings x) (cons 'horizontals y)))))))

#(define (tuplet-bracket::wing-thickness wing-thickness)
  "Examine @code{TupletBracket.stencil), replace the wings by a polygon
mimicking enlarged thickness."
 (grob-transformer 'stencil
  (lambda (grob orig)
   (let* ((parts (tuplet-bracket::line-parts grob orig))
          (raw-wings (assoc-get 'wings parts)))
     (if (not (pair? raw-wings))
         orig
         (let* (
          (horizontals (assoc-get 'horizontals parts))
          (slopes
           (map
            (lambda (l)
              (/ (- (list-ref l 5) (list-ref l 3))
                 (- (list-ref l 4) (list-ref l 2))))
            horizontals))
          (wings
           (cond ((middle-broken-spanner? grob) '(#f #f))
                 ((first-broken-spanner? grob)
                   (append raw-wings (list #f)))
                 ((end-broken-spanner? grob)
                   (cons #f raw-wings))
                 (else raw-wings)))
          (grob-thick
           (ly:grob-property grob 'thickness))
          (staff-line-thick
           (ly:staff-symbol-line-thickness (ly:grob-object grob 'staff-symbol)))
          (thick (* grob-thick staff-line-thick))
          (edge-height (ly:grob-property grob 'edge-height))
          (shorten-pair (ly:grob-property grob 'shorten-pair '(0 . 0)))
          (dir (ly:grob-property grob 'direction))
          (staff-space (ly:staff-symbol-staff-space grob)))

    (ly:make-stencil
     (lists-map
      (lambda (l)
       (cond
        ((equal? l (car wings))
          (let* ((start-x (list-ref l 2))
                 (start-y (+ (list-ref l 3) (* wing-thickness (car slopes))))
                 (shorten-pair (car shorten-pair))
                 (edge-height (* staff-space (car edge-height))))
            `(polygon
              ,(list
                start-x (list-ref l 3)
                (+ start-x wing-thickness) start-y
                (+ start-x wing-thickness) (+ start-y (* -1 dir edge-height))
                start-x (+ (list-ref l 3) (* dir -1 edge-height)))
              ;; take `thick` as blot-diameter to match rounded line ends
              ,thick
              #t)))
        ((equal? l (cadr wings))
          (let* ((end-x (list-ref l 2))
                 (start-x (- end-x wing-thickness))
                 (start-y (* start-x (cadr slopes)))
                 (end-y (list-ref l 5))
                 (edge-height (* staff-space (cdr edge-height))))
            `(polygon
               ,(list
                 end-x end-y
                 end-x (- end-y (* dir -1 edge-height))
                 start-x start-y
                 start-x (+ start-y (* dir -1 edge-height)))
               ,thick
               #t)))
        (else l)))
      (ly:stencil-expr orig))
     (ly:stencil-extent orig X)
     (ly:stencil-extent orig Y))))))))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Examples
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\layout {
  \override TupletBracket.stencil = #(tuplet-bracket::wing-thickness 1)
}

{
  \tuplet 3/2 { b4 b b } \tuplet 3/2 { b'' b b } \tuplet 3/2 { b b b'' }
  \tupletDown
  \tuplet 3/2 { b4 b b } \tuplet 3/2 { b'' b b } \tuplet 3/2 { b b b'' }
}

{
  \tuplet 3/2 { b1 b''2 \break b4 b \break b''2 b }
}

\score {
\new Score <<
\new Staff
  \with {
    %{ proportionalNotationDuration = #(ly:make-moment 1 40) %}
    fontSize = #-2
    \override StaffSymbol.staff-space=#(magstep -2)
  }
  {

    \tuplet 3/2 { b4 b b } \tuplet 3/2 { b'' b b } \tuplet 3/2 { b b b'' }
    \tupletDown
    \tuplet 3/2 { b4 b b } \tuplet 3/2 { b'' b b } \tuplet 3/2 { b b b'' }
  }
>>
}
