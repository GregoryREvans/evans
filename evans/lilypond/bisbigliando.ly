\version "2.19.84"
\language "english"

\new Staff {
  c''1
	- \tweak bound-details.left.text \markup{ \raise #1 \teeny \musicglyph #"scripts.halfopenvertical" }
	\startTrillSpan
  c''1
	\stopTrillSpan
  c''1
	- \tweak bound-details.left.text \markup {
		\lower #1.5
		\override #'(graphical . #t)
		\override #'(size . 0.4)
		\override #'(thickness . 0.25)
	    \woodwind-diagram
	        #'flute
	        #'((cc . (one two three four five six)) (lh . (bes b gis)) (rh . (bes d dis ees cis c gz)))
	    }
	\startTrillSpan
  c''1
	\stopTrillSpan
}
