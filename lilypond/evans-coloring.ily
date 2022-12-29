\version "2.23.14" % temp
evans-not-yet-pitched-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'goldenrod
    $music
    #}
    )

evans-pitch-out-of-range-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

evans-time-signature-color = #(
    define-music-function
    (parser location color music)
    (symbol? ly:music?)
    #{
    \once \override Score.TimeSignature.color = #(x11-color #'color)
    $music
    #}
    )

%%% color until reverted %%%
all-color-music = #(
    define-music-function (parser location color music) (color? ly:music?)
    #{
    \override Accidental.color = $color
    \override Beam.color = $color
    \override Dots.color = $color
    \override Flag.color = $color
    \override Glissando.color = $color
    \override MultiMeasureRest.color = $color
    \override NoteHead.color = $color
    \override NoteHead.details.hocket-color = $color
    \override NoteHead.details.interrupt-color = $color
    \override RepeatTie.color = $color
    \override Rest.color = $color
    \override Slur.color = $color
    \override Stem.color = $color
    \override StemTremolo.color = $color
    \override Tie.color = $color
    $music
    #}
    )

safe-blue = #(rgb-color 49/110 63/110 77/110)
safe-green = #(rgb-color 49/110 77/110 63/110)
safe-red = #(rgb-color 77/110 49/110 63/110)
