\version "2.19.82"

#(define-public ((tuplet-number::append-note-wrapper function note) grob)
  (let* ((txt (function grob)))
    (markup txt #:fontsize -5 #:note note UP)))

{
  \override TupletNumber #'text = #(tuplet-number::append-note-wrapper
                            tuplet-number::calc-fraction-text "4")
  \times 2/3 {c'4 c' c'}
  \times 2/3 {c' c' c'}

  \override TupletNumber #'text = #(tuplet-number::append-note-wrapper
                         tuplet-number::calc-fraction-text "8")
  \times 2/3 {c'8 c' c'}
  \times 4/6 {c'4:8 c'4:8 c'4:8}
  \times 2/3 {c'8 c'8 c'8}
  \times 2/3 {c'4 c' c'}
  \times 8/12 {c':16 c':16 c':16}

  \override TupletNumber #'text = #(tuplet-number::append-note-wrapper
                        tuplet-number::calc-denominator-text "8")
  \times 2/3 {c'8 c' c'}
  \times 4/6 {c'4:8 c'4:8 c'4:8}
}
