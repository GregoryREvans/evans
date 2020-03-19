\version "2.19.84"
\language "english"
#(set-default-paper-size "11x17landscape")
#(set-global-staff-size 20)
\include "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"
\include "evans-markups.ily"
\include "evans-spanners.ily"

\layout {
	\context {
		\Score
		proportionalNotationDuration = #(ly:make-moment 1 60)
	}
}

\new Score {
	\new StaffGroup <<
		\new Staff {
			c'4
				- \abjad-solid-line-with-arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                             \evans-counterclockwise-arc
							\translate #'(0.2 . 0.75)
							\scale #'(0.4 . 0.4)
							\concat {
								\translate #'(0 . 0)
								0
								\translate #'(0 . 1)
								\teeny o
								\hspace #0.5
								}
                            }
                        }
                    - \tweak bound-details.right.padding 1.4
                    - \tweak staff-padding #2
                    \startTextSpanOne
			c'4
				\stopTextSpanOne
				- \abjad-solid-line-with-arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                            \evans-clockwise-arc
							\translate #'(0 . 0.75)
							\scale #'(0.4 . 0.4)
							\concat {
								\translate #'(0 . 0.3)
								-
								\translate #'(0 . 0)
								45
								\translate #'(0 . 1)
								\teeny o
								\hspace #0.5
								}
							}
                        }
                    - \tweak bound-details.right.padding 1.4
                    - \tweak staff-padding #2
                    \startTextSpanOne
			c'4
				\stopTextSpanOne
				- \abjad-solid-line-with-arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                            \evans-clockwise-arc
							\translate #'(0 . 0.75)
							\scale #'(0.4 . 0.4)
							\concat {
								\translate #'(0 . 0)
								45
								\translate #'(0 . 1)
								\teeny o
								\hspace #0.5
								}
							}
                        }
                    - \tweak bound-details.right.padding 1.4
                    - \tweak staff-padding #2
                    \startTextSpanOne
			c'4
				\stopTextSpanOne
				- \abjad-solid-line-with-arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                            \evans-counterclockwise-arc
							\translate #'(0 . 0.75)
							\scale #'(0.4 . 0.4)
							\concat {
								\translate #'(0 . 0)
								60
								\translate #'(0 . 1)
								\teeny o
								\hspace #0.5
								}
							}
                        }
                    - \tweak bound-details.right.padding 1.4
                    - \tweak staff-padding #2
                    \startTextSpanOne
			r2
				\stopTextSpanOne
				- \abjad-invisible-line
                    - \tweak bound-details.left.text \markup {
                      	\translate #'(0 . 0.75)
							\scale #'(0.4 . 0.4)
							\concat {
								\translate #'(0 . 0)
								0
								\translate #'(0 . 1)
								\teeny o
								\hspace #0.5
								}
                        }
                    - \tweak bound-details.right.padding 1.4
                    - \tweak staff-padding #2
                    \startTextSpanOne
			r2
				\stopTextSpanOne
		}
		\new Staff {
			c'4
			- \abjad-solid-line-with-arrow
			- \evans-counterclockwise-BAD-spanner-left-text #0
			- \tweak bound-details.right.padding 1.4
			- \tweak staff-padding #2
			\evansStartTextSpanBAD
			c'4
			\evansStopTextSpanBAD
			- \abjad-solid-line-with-arrow
			- \evans-clockwise-BAD-spanner-left-text #-45
			- \tweak bound-details.right.padding 1.4
			- \tweak staff-padding #2
			\evansStartTextSpanBAD
			c'4
			\evansStopTextSpanBAD
			- \abjad-solid-line-with-arrow
			- \evans-clockwise-BAD-spanner-left-text #45
			- \tweak bound-details.right.padding 1.4
			- \tweak staff-padding #2
			\evansStartTextSpanBAD
			c'4
			\evansStopTextSpanBAD
			- \abjad-solid-line-with-arrow
			- \evans-counterclockwise-BAD-spanner-left-text #60
			- \evans-BAD-spanner-right-text #0
			- \tweak bound-details.right.padding 3
			- \tweak staff-padding #2
			\evansStartTextSpanBAD
			r1
			\evansStopTextSpanBAD
		}
	>>
}
