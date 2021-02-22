import abjad
import evans
from abjadext import rmakers

score = abjad.Score(
    [
        abjad.StaffGroup(
            [
                abjad.Staff(
                    [
                        abjad.Voice(
                            "c'4 c'4 c'4 c'4",
                            name="Voice 1",
                        )
                    ],
                    name="Staff 1",
                ),
                abjad.Staff(
                    [
                        abjad.Voice(
                            "c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8",
                            name="Voice 2",
                        )
                    ],
                    name="Staff 2",
                ),
            ],
            name="group",
        )
    ],
    name="Score",
)

h = evans.IntermittentVoiceHandler(
    evans.RhythmHandler(
        rmakers.stack(
            evans.RTMMaker(
                [
                    "(1 (1 1 1))",
                ]
            ),
        ),
        forget=False,
    ),
    direction=abjad.Up,
)

selector = abjad.select().leaf(1)
target = selector(score["Voice 1"])
h(target)

abjad.show(score)
