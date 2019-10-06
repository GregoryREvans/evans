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

%%% five eighth tones down %%%
five-eighths-flat =
#(define-music-function (parser location note)   (ly:music?)
 #{ \once \override Voice.Accidental.stencil =
          #ly:text-interface::print
        \once \override Voice.Accidental.text =
          \markup {\musicglyph #"accidentals.flat.arrowdown"}
        $note #})

%%% seven eighth tones down %%%

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

%%% two thirds down %%%

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
