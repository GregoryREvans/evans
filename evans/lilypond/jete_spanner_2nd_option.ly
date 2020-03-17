\version "2.19.84"
\include "evans-articulations.ily"
\include "evans-markups.ily"

\score {
	\new Score <<
		\new Staff{
			c'2
				\ferneyhough-gettato
			c''2
				\piston-jete
	}
	>>
}
