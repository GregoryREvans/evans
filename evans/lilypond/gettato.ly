\version "2.19.84"  %! abjad.LilyPondFile._get_format_pieces()
\language "english" %! abjad.LilyPondFile._get_format_pieces()
\include "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"

\header { %! abjad.LilyPondFile._get_formatted_blocks()
    tagline = ##f
} %! abjad.LilyPondFile._get_formatted_blocks()

\layout {
\context {
\Score
   proportionalNotationDuration = #(ly:make-moment 1 70)
}
}

\paper {}

\score { %! abjad.LilyPondFile._get_formatted_blocks()
\new StaffGroup <<
    \new Staff
    {
        \context Voice = "Music_Voice"
        {
            c'4
            <<
                \context Voice = "On_Beat_Grace_Container"
                {
                    \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                    \slash %! abjad.on_beat_grace_container(2)
                    \voiceOne %! abjad.on_beat_grace_container(3)
					\once \override Beam.grow-direction = #left
                    <
                        \tweak font-size #0
                        \tweak transparent ##t
                        d'
						\tweak transparent ##t
                        g''
                    >32 * 2/3
					^ \markup {\hspace #1 thrown gett. (21)}
                    [
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3

                    ]
                }
                \context Voice = "Music_Voice"
                {
                    \voiceTwo %! abjad.on_beat_grace_container(4)
                    d'4
                    e'4
                }
            >>
            \oneVoice %! abjad.on_beat_grace_container(5)
            f'4
        }
    }
\new Staff
    {
        \context Voice = "Music_Voice"
        {
            c'4
            <<
                \context Voice = "On_Beat_Grace_Container"
                {
                    \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                    \slash %! abjad.on_beat_grace_container(2)
                    \voiceOne %! abjad.on_beat_grace_container(3)
					\once \override Beam.grow-direction = #right
                    <
                        \tweak font-size #0
                        \tweak transparent ##t
                        d'
						\tweak transparent ##t
                        g''
                    >32 * 2/3
					^ \markup {\hspace #1 dropped gett. (21)}
                    [
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
					\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3
\tweak transparent ##t
                    g''32 * 2/3

                    ]
                }
                \context Voice = "Music_Voice"
                {
                    \voiceTwo %! abjad.on_beat_grace_container(4)
                    d'4
                    e'4
                }
            >>
            \oneVoice %! abjad.on_beat_grace_container(5)
            f'4
        }
    }
>>
} %! abjad.LilyPondFile._get_formatted_blocks()