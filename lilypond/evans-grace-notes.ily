\version "2.23.81"


%%% my hack slash %%%
my-hack-slash = {
 \once \override Stem.stencil =
   #(lambda (grob)
      (let* ((x-parent (ly:grob-parent grob X))
             (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
        (if is-rest?
            empty-stencil
            (ly:stencil-combine-at-edge
             (ly:stem::print grob)
             Y
             (+ (ly:grob-property grob 'direction))
             (grob-interpret-markup grob
                                    (markup #:hspace 0.25 #:fontsize 3
                                            #:musicglyph "flags.ugrace"))
             -0.9))))
}

my-ob-hack-slash = {
 \once \override Stem.stencil =
   #(lambda (grob)
      (let* ((x-parent (ly:grob-parent grob X))
             (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
        (if is-rest?
            empty-stencil
            (ly:stencil-combine-at-edge
             (ly:stem::print grob)
             Y
             (+ (ly:grob-property grob 'direction))
             (grob-interpret-markup grob
                                    (markup #:hspace 0.4 #:fontsize 1.5
                                            #:musicglyph "flags.ugrace"))
             -1.05))))
}

my-hack-flag = {
 \override Stem.stencil =
   #(lambda (grob)
      (let* ((x-parent (ly:grob-parent grob X))
             (is-rest? (ly:grob? (ly:grob-object x-parent 'rest))))
        (if is-rest?
            empty-stencil
            (ly:stencil-combine-at-edge
             (ly:stem::print grob)
             Y
             (+ (ly:grob-property grob 'direction))
             (grob-interpret-markup grob
                                    (markup #:hspace 0.05 #:fontsize -1 #:combine
                                            #:musicglyph "flags.ugrace" #:musicglyph "flags.u3"))
             -1.93))))
}

startAcciaccaturaMusic = { % single grace
  %{ \override GraceSpacing.spacing-increment = #0.1 %}
  \my-hack-flag
  \override Beam.transparent = ##t
  \override Stem.Y-extent = #'(0 . 0) % new
  \override NoteHead.layer = #3
  \override Stem.layer = #2
  \override Stem.whiteout-style = #'outline
  \override Stem.whiteout = 1
  \override Stem.direction = #UP
  \override Rest.stencil = ##f
  \override Rest.X-extent = ##f
  \slurHalfDashed
}

stopAcciaccaturaMusic = {
  %{ \revert GraceSpacing.spacing-increment %}
  \revert Stem.stencil
  \revert Beam.transparent
  \revert Stem.Y-extent % new
  \revert NoteHead.layer
  \revert Stem.layer
  \revert Stem.whiteout-style
  \revert Stem.whiteout
  \revert Stem.direction
  \revert Rest.stencil
  \revert Rest.X-extent
  \slurSolid
  <>)
}

startAppoggiaturaMusic = { % multi grace
  <>(
  \my-hack-slash
  \overhead-accidentals #-3
  \override Beam.Y-extent = #'(0 . 0) % new
  \override Stem.Y-extent = #'(0 . 0) % new
  \override NoteHead.layer = #3
  \override Beam.layer = #3
  \override Stem.layer = #2
  \override Stem.whiteout-style = #'outline
  \override Stem.whiteout = 1
  \override Stem.direction = #UP
  \slurHalfDashed

}

stopAppoggiaturaMusic = {
  \normal-accidentals #-2
  \revert Beam.Y-extent % new
  \revert Stem.Y-extent % new
  \revert NoteHead.layer
  \revert Beam.layer
  \revert Stem.layer
  \revert Stem.whiteout-style
  \revert Stem.whiteout
  \revert Stem.direction
  \slurSolid
  <>)
}

start-single-grace = {
    \my-hack-flag
    \override Beam.transparent = ##t
    \override Stem.Y-extent = #'(0 . 0) % new
    \override NoteHead.layer = #3
    \override Stem.layer = #2
    \override Stem.whiteout-style = #'outline
    \override Stem.whiteout = 1
    \override Stem.direction = #UP
    %{ \override Rest.transparent = ##t %}
    %{ \override Rest.X-extent = ##f %}
}

stop-single-grace = {
    \revert Stem.stencil
    \revert Beam.transparent
    \revert Stem.Y-extent % new
    \revert NoteHead.layer
    \revert Stem.layer
    \revert Stem.whiteout-style
    \revert Stem.whiteout
    \revert Stem.direction
    %{ \revert Rest.transparent %}
    %{ \revert Rest.X-extent %}
}

start-multi-grace = {
    \my-hack-slash
    \overhead-accidentals #-3
    \override Beam.Y-extent = #'(0 . 0) % new
    \override Stem.Y-extent = #'(0 . 0) % new
    \override NoteHead.layer = #3
    \override Beam.layer = #3
    \override Stem.layer = #2
    \override Stem.whiteout-style = #'outline
    \override Stem.whiteout = 1
    \override Stem.direction = #UP
}

stop-multi-grace = {
    \normal-accidentals #-2
    \revert Beam.Y-extent % new
    \revert Stem.Y-extent % new
    \revert NoteHead.layer
    \revert Beam.layer
    \revert Stem.layer
    \revert Stem.whiteout-style
    \revert Stem.whiteout
    \revert Stem.direction
}

start-ob-multi-grace = {
    \my-ob-hack-slash
    \override Beam.Y-extent = #'(0 . 0) % new
    \override Slur.Y-extent = #'(0 . 0) % new
    \override Stem.Y-extent = #'(0 . 0) % new
    \override NoteHead.layer = #3
    \override Beam.layer = #3
    \override Stem.layer = #2
    \override Stem.whiteout-style = #'outline
    \override Stem.whiteout = 1
    \override Stem.direction = #UP
    \slurHalfDashed
}

stop-ob-multi-grace = {
    \revert Beam.Y-extent % new
    \revert Slur.Y-extent % new
    \revert Stem.Y-extent % new
    \revert NoteHead.layer
    \revert Beam.layer
    \revert Stem.layer
    \revert Stem.whiteout-style
    \revert Stem.whiteout
    \revert Stem.direction
    \slurSolid
}
