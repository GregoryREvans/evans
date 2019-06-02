%% http://lsr.di.unimi.it/LSR/Item?id=721
%% see also http://lilypond.org/doc/v2.18/Documentation/notation/special-rhythmic-concerns
%% see also http://lilypond.1069038.n5.nabble.com/LSR-v2-18-quot-Slashed-beamed-grace-notes-quot-enhancement-proposal-tc159585.html


%LSR contributed by David Nalesnik (see http://lilypond.1069038.n5.nabble.com/So-slashed-beamed-grace-notes-td152817.html)
%LSR original contributed by Valentin Villenave

% The argument `ang' is the amount of slant, expressed in degrees.
%
% Stem-fraction is the distance between the point the slash crosses the stem
% and the notehead-end of the stem.  It is expressed as a number between 0 and 1.
%
% The argument `protrusion' is the extra distance the slash
% extends beyond its intersection with stem and beam

slash =
#(define-music-function (parser location ang stem-fraction protrusion)
   (number? number? number?)
   (remove-grace-property 'Voice 'Stem 'direction) ; necessary?
   #{
     \once \override Stem #'stencil =
     #(lambda (grob)
       (let* ((X-parent (ly:grob-parent grob X))
              (is-rest? (ly:grob? (ly:grob-object X-parent 'rest))))
         (if is-rest?
             empty-stencil
             (let* ((ang (degrees->radians ang))
                    ; We need the beam and its slope so that slash will
                    ; extend uniformly past the stem and the beam
                    (beam (ly:grob-object grob 'beam))
                    (beam-X-pos (ly:grob-property beam 'X-positions))
                    (beam-Y-pos (ly:grob-property beam 'positions))
                    (beam-slope (/ (- (cdr beam-Y-pos) (car beam-Y-pos))
                                   (- (cdr beam-X-pos) (car beam-X-pos))))
                    (beam-angle (atan beam-slope))
                    (stem-Y-ext (ly:grob-extent grob grob Y))
                    ; Stem.length is expressed in half staff-spaces
                    (stem-length (/ (ly:grob-property grob 'length) 2.0))
                    (dir (ly:grob-property grob 'direction))
                    ; if stem points up. car represents segment of stem
                    ; closest to notehead; if down, cdr does
                    (stem-ref (if (= dir 1) (car stem-Y-ext) (cdr stem-Y-ext)))
                    (stem-segment (* stem-length stem-fraction))
                    ; Where does slash cross the stem?
                    (slash-stem-Y (+ stem-ref (* dir stem-segment)))
                    ; These are values for the portion of the slash that
                    ; intersects the beamed group.
                    (dx (/ (- stem-length stem-segment)
                           (- (tan ang) (* dir beam-slope))))
                    (dy (* (tan ang) dx))
                    ; Now, we add in the wings
                    (protrusion-dx (* (cos ang) protrusion))
                    (protrusion-dy (* (sin ang) protrusion))
                    (x1 (- protrusion-dx))
                    (y1 (- slash-stem-Y (* dir protrusion-dy)))
                    (x2 (+ dx protrusion-dx))
                    (y2 (+ slash-stem-Y
                           (* dir (+ dy protrusion-dy))))
                    (th (ly:staff-symbol-line-thickness grob))
                    (stil (ly:stem::print grob)))

              (ly:stencil-add
                stil
                (make-line-stencil th x1 y1 x2 y2))))))
   #})

slashI = {
  \slash 50 0.6 1.0
}

slashII = {
  \slash 45 0.5 0.8
}

\layout {
  ragged-right = ##t
}

\new Staff {
  \relative c' {
    \acciaccatura { \slashI d8[ e f g] } d4
    \acciaccatura { \slashI g8[ a b c] } d4
    \acciaccatura { \slashI g8[ a b c] } d4
    \acciaccatura { \slashI g8[ a b c ] } d4
    \clef bass
    \acciaccatura { \slashII d,,,8[ c b a ] } g4
    \acciaccatura { \slashII d8[ c b a ] } g4
    \acciaccatura { \slashII d8[ c b a ] } g4
    \acciaccatura { \slashII d8[ c b a ] } g4
  }
}

\new Staff {
  \relative c'' {
    \acciaccatura {
      \slash 50 0.4 1
      dis32[ e, a' bes, cis, d' ]
    }
    es,4
  }
}

\new PianoStaff <<
  \new Staff = "1" {
    s1*0
    \grace {
      \slash 65 0.8 1.5
      \stemDown
      a'''16[
      \change Staff = "2"
      \stemUp
      bes,
      \change Staff = "1"
      \stemDown
      fis''16
      \change Staff = "2"
      \stemUp
      g]
    }
    \change Staff = "1"
    es'4
  }
  \new Staff = "2" {
    \clef bass
    \grace s4
    s4
  }
>>
