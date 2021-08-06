%%% BREAKS %%%

evans-lbsd = #(
    define-music-function
    (parser location y-offset distances)
    (number? list?)
    #{
    \overrideProperty
    Score.NonMusicalPaperColumn.
    line-break-system-details.Y-offset
    #y-offset
    \overrideProperty
    Score.NonMusicalPaperColumn.
    line-break-system-details.alignment-distances
    #distances
    #}
    )

evans-system-X-offset = #(
    define-music-function
    (parser location x-offset)
    (number?)
    #{
    \overrideProperty
    Score.NonMusicalPaperColumn.
    line-break-system-details.X-offset
    #x-offset
    #}
    )

%%% SPACING SECTIONS %%%

evans-new-spacing-section = #(
    define-music-function
    (parser location n d music)
    (number? number? ly:music?)
    #{
    \set Score.proportionalNotationDuration = #(ly:make-moment n d)
    \newSpacingSection
    $music
    #}
    )
