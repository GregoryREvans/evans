\version "2.19.83"
\language "english"

parentheAll = #(define-music-function (parser location note) (ly:music?)
#{
  \once \override ParenthesesItem.font-size = #-1
  \once \override ParenthesesItem.stencil = #(lambda (grob)
       (let* ((acc (ly:grob-object (ly:grob-parent grob Y) 'accidental-grob))
              (dot (ly:grob-object (ly:grob-parent grob Y) 'dot)))
         (if (not (null? acc)) (ly:pointer-group-interface::add-grob grob 'elements acc))
         (if (not (null? dot)) (ly:pointer-group-interface::add-grob grob 'elements dot))
         (parentheses-item::print grob)))
  \parenthesize $note
#})

\score {
    \new Staff {
        \pitchedTrill b2 \startTrillSpan
        -\tweak minimum-length #10 %?
        -\tweak springs-and-rods #ly:spanner::set-spacing-rods %?
        -\tweak bound-details.right.Y #-2.7 %?
        -\tweak bound-details.left.padding #3.5 %?
        -\tweak bound-details.right.padding #.8 %?
        \glissando ~ c'
        \once \omit Staff.Flag
        \once \omit Staff.Stem
        \once \override NoteHead.font-size = #-4
        \once \override NoteHead.X-offset = #-.4
        \grace {  \parentheAll cs'!8\stopTrillSpan }
        b8 r8
    }
}
