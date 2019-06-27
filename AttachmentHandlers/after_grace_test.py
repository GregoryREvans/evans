import abjad

voice = abjad.Voice("c'4 d'4 e'4 f'4")

for run in abjad.select(voice).runs():
    string = "#(define afterGraceFraction (cons 15 16))"
    literal = abjad.LilyPondLiteral(string)
    abjad.attach(literal, run[0])
    grace_note = [abjad.Note("c'8")]
    after_grace_container = abjad.AfterGraceContainer(grace_note)
    notehead_literal = abjad.LilyPondLiteral(
        r"\once \override NoteHead.transparent = ##t", format_slot="before"
    )
    stem_literal = abjad.LilyPondLiteral(
        r"\once \override Stem.transparent = ##t", format_slot="before"
    )
    flag_literal = abjad.LilyPondLiteral(
        r"\once \override Flag.transparent = ##t", format_slot="before"
    )
    start_command = abjad.LilyPondLiteral(
        r"""\stopStaff \once \override Staff.LedgerLineSpanner #'color = #white  \startStaff""",
        format_slot="before",
    )
    stop_command = abjad.LilyPondLiteral(r"\stopStaff \startStaff", format_slot="after")
    abjad.attach(notehead_literal, after_grace_container[0])
    abjad.attach(stem_literal, after_grace_container[0])
    abjad.attach(flag_literal, after_grace_container[0])
    abjad.attach(start_command, after_grace_container[0])
    abjad.attach(stop_command, after_grace_container[0])
    abjad.attach(after_grace_container, run[-1])

abjad.show(voice)
