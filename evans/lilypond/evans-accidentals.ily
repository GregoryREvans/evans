%%% one eighth tone up %%%
one-eighth-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.natural.arrowup"}
        $note #})

%%% three eighth tones up %%%
three-eighths-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.sharp.slashslash.stem"
       \postscript #"gsave 0.17 setlinewidth -0.95 1.25 moveto -0.95 2 lineto
       stroke grestore
       gsave 0.1 setlinewidth -1.25 1.4 moveto -0.95 2.18 lineto -0.65 1.4 lineto
       stroke grestore"}
        $note #})

%%% five eighth tones up %%%
five-eighths-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.sharp.arrowup"}
        $note #})

%%% seven eighth tones up %%%
seven-eighths-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.sharp.slashslash.stemstemstem"
          \postscript #"gsave 0.17 setlinewidth -0.95 1.25 moveto -0.95 2 lineto
          stroke grestore
          gsave 0.1 setlinewidth -1.25 1.4 moveto -0.95 2.18 lineto -0.65 1.4 lineto
          stroke grestore"}
        $note #})

%%% one eighth tone down %%%
one-eighth-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.natural.arrowdown"}
        $note #})

%%% three eighth tones down %%%
three-eighths-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.mirroredflat"
       \postscript #"gsave 0.15 setlinewidth -0.73 -0.25 moveto -0.73 -1.4 lineto
       stroke grestore
       gsave 0.1 setlinewidth -1.03 -0.7 moveto -0.73 -1.48 lineto -0.43 -0.7 lineto
       stroke grestore"}
        $note #})

%%% five eighth tones down %%%
five-eighths-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.flat.arrowdown"}
        $note #})

%%% seven eighth tones down %%%
seven-eighths-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.mirroredflat.flat"
       \postscript #"gsave 0.15 setlinewidth -1.40 -0.25 moveto -1.40 -1.4 lineto
       stroke grestore
       gsave 0.1 setlinewidth -1.70 -0.7 moveto -1.40 -1.48 lineto -1.10 -0.7 lineto
       stroke grestore"}
        $note #})

%%% one third up %%%
one-third-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 1 3
              \postscript #"gsave 0.17 setlinewidth -0.95 1.25 moveto -0.95 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.25 1.4 moveto -0.95 2.18 lineto -0.65 1.4 lineto
              stroke grestore"}
        $note #})

%%% two thirds up %%%
two-thirds-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 2 3
              \postscript #"gsave 0.17 setlinewidth -0.95 1.25 moveto -0.95 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.25 1.4 moveto -0.95 2.18 lineto -0.65 1.4 lineto
              stroke grestore"}
        $note #})

%%% one third down %%%
one-third-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 1 3
              \postscript #"gsave 0.15 setlinewidth -1 -1.35 moveto -1 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.30 -1.4 moveto -1 -2.18 lineto -0.7 -1.4 lineto
              stroke grestore"}
        $note #})

%%% two thirds down %%%
two-thirds-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 2 3
              \postscript #"gsave 0.15 setlinewidth -1 -1.35 moveto -1 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.30 -1.4 moveto -1 -2.18 lineto -0.7 -1.4 lineto
              stroke grestore"}
        $note #})

%%% one sixth up %%%
one-sixth-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 1 6
              \postscript #"gsave 0.17 setlinewidth -0.95 1.25 moveto -0.95 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.25 1.4 moveto -0.95 2.18 lineto -0.65 1.4 lineto
              stroke grestore"}
        $note #})

%%% five sixths up %%%
five-sixths-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 5 6
              \postscript #"gsave 0.17 setlinewidth -0.95 1.25 moveto -0.95 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.25 1.4 moveto -0.95 2.18 lineto -0.65 1.4 lineto
              stroke grestore"}
        $note #})

%%% one sixth down %%%
one-sixth-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 1 6
              \postscript #"gsave 0.15 setlinewidth -1 -1.35 moveto -1 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.30 -1.4 moveto -1 -2.18 lineto -0.7 -1.4 lineto
              stroke grestore"}
        $note #})

%%% five sixths down %%%
five-sixths-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 5 6
              \postscript #"gsave 0.15 setlinewidth -1 -1.35 moveto -1 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.30 -1.4 moveto -1 -2.18 lineto -0.7 -1.4 lineto
              stroke grestore"}
        $note #})

%%% one twelf up %%%
one-twelf-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 1 12
              \postscript #"gsave 0.17 setlinewidth -1.35 1.25 moveto -1.35 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.65 1.4 moveto -1.35 2.18 lineto -1.05 1.4 lineto
              stroke grestore"}
        $note #})

%%% five twelfs up %%%
five-twelfs-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 5 12
              \postscript #"gsave 0.17 setlinewidth -1.35 1.25 moveto -1.35 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.65 1.4 moveto -1.35 2.18 lineto -1.05 1.4 lineto
              stroke grestore"}
        $note #})

%%% seven twelfs up %%%
seven-twelfs-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 7 12
              \postscript #"gsave 0.17 setlinewidth -1.35 1.25 moveto -1.35 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.65 1.4 moveto -1.35 2.18 lineto -1.05 1.4 lineto
              stroke grestore"}
        $note #})

%%% eleven twelfs up %%%
eleven-twelfs-sharp =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 11 12
              \postscript #"gsave 0.17 setlinewidth -1.35 1.25 moveto -1.35 2 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.65 1.4 moveto -1.35 2.18 lineto -1.05 1.4 lineto
              stroke grestore"}
        $note #})

%%% one twelf down %%%
one-twelf-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 1 12
              \postscript #"gsave 0.15 setlinewidth -1.40 -1.35 moveto -1.40 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.70 -1.4 moveto -1.40 -2.18 lineto -1.10 -1.4 lineto
              stroke grestore"}
        $note #})

%%% five twelfs down %%%
five-twelfs-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 5 12
              \postscript #"gsave 0.15 setlinewidth -1.40 -1.35 moveto -1.40 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.70 -1.4 moveto -1.40 -2.18 lineto -1.10 -1.4 lineto
              stroke grestore"}
        $note #})

%%% seven twelfs down %%%
seven-twelfs-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 7 12
              \postscript #"gsave 0.15 setlinewidth -1.40 -1.35 moveto -1.40 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.70 -1.4 moveto -1.40 -2.18 lineto -1.10 -1.4 lineto
              stroke grestore"}
        $note #})

%%% eleven twelfs down %%%
eleven-twelfs-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\fontsize #-4
              \translate #'(0 . -0.5) \fraction 11 12
              \postscript #"gsave 0.15 setlinewidth -1.40 -1.35 moveto -1.40 -2.1 lineto
              stroke grestore
              gsave 0.1 setlinewidth -1.70 -1.4 moveto -1.40 -2.18 lineto -1.10 -1.4 lineto
              stroke grestore"}
        $note #})
