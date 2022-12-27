\version "2.23.81"


old-bass-clef =
#(ly:make-stencil
  `(path 0.001
     (moveto   -0.10  -0.35
      curveto  -0.10  -1.11   0.48  -1.80   1.25  -1.80
      curveto   1.75  -1.80   2.20  -1.60   2.50  -1.05
      curveto   2.55  -0.95   2.50  -0.90   2.43  -0.95
      curveto   2.20  -1.17   1.90  -1.48   1.45  -1.48
      curveto   0.70  -1.48   0.15  -0.85   0.15  -0.15
      curveto   0.15   0.45   0.62   0.83   1.05   0.83
      curveto   1.55   0.83   1.90   0.50   1.90   0.05
      curveto   1.90  -0.35   1.55  -0.71   1.20  -0.71
      curveto   0.80  -0.71   0.60  -0.40   0.63  -0.17
      curveto   0.75  -0.30   0.90  -0.31   1.00  -0.31
      curveto   1.20  -0.31   1.38  -0.10   1.38   0.15
      curveto   1.38   0.35   1.20   0.55   0.95   0.55
      curveto   0.60   0.52   0.39   0.25   0.39  -0.05
      curveto   0.39  -0.52   0.62  -0.89   1.20  -0.89
      curveto   1.65  -0.89   2.07  -0.50   2.07   0.10
      curveto   2.07   0.66   1.56   1.01   1.05   1.01
      curveto   0.28   1.01  -0.10   0.35  -0.10  -0.35
      moveto    2.42   0.20
      curveto   2.54   0.20   2.64   0.30   2.64   0.42
      curveto   2.64   0.54   2.54   0.64   2.42   0.64
      curveto   2.30   0.64   2.20   0.54   2.20   0.42
      curveto   2.20   0.30   2.30   0.20   2.42   0.20
      moveto    2.42  -0.20
      curveto   2.54  -0.20   2.64  -0.30   2.64  -0.42
      curveto   2.64  -0.54   2.54  -0.64   2.42  -0.64
      curveto   2.30  -0.64   2.20  -0.54   2.20  -0.42
      curveto   2.20  -0.30   2.30  -0.20   2.42  -0.20
      closepath)
     round round #t)
   (cons -0.1 2.65)
   (cons -1.3 1))



old-g-clef-markup = \markup {
          \general-align #Y #-0.5
          \epsfile #Y #5.5 #"gfx/old-g-clef.eps"
      }

old-g-clef-markup-change = \markup {
        \general-align #Y #-0.5
        \epsfile #Y #2.5 #"gfx/old-g-clef.eps"
    }

mendelssohn-g-clef-markup = \markup {
         \general-align #Y #-0.7
         \epsfile #Y #6.5 #"gfx/mendelssohn-treble.eps"
     }

alt-g-clef-markup = \markup {
       \general-align #Y #-0.2
       \epsfile #Y #7 #"gfx/alt-treble.eps"
   }


behind-bridge-clef-markup = \markup {
      \general-align #Y #-0.2
      \epsfile #Y #7 #"gfx/behind-bridge-clef.eps"
  }
