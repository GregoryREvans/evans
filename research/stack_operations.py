import abjad
import evans
from abjadext import rmakers

rmaker = rmakers.talea([1, 3, 2, 4, 5], 8, extra_counts=[1, 0, 1, 1, 2, 3, 4])


def quarters(divisions):
    divisions = evans.BacaSequence(divisions)
    divisions = evans.BacaSequence(evans.BacaSequence(_).quarters() for _ in divisions)
    divisions = evans.BacaSequence(divisions).flatten(depth=-1)
    return divisions


commands = [
    rmakers.trivialize(lambda _: abjad.select.tuplets(_)),
    rmakers.rewrite_rest_filled(lambda _: abjad.select.tuplets(_)),
    rmakers.rewrite_sustained(lambda _: abjad.select.tuplets(_)),
    rmakers.extract_trivial(),
    rmakers.RewriteMeterCommand(
        boundary_depth=-1,
        reference_meters=[
            abjad.Meter((6, 8)),
            abjad.Meter((9, 8)),
        ],
    ),
]

stack = rmakers.stack(
    rmaker,
    *commands,
    preprocessor=quarters,
)

divisions = [(6, 8), (9, 8)]

selections = stack(divisions)

lilypond_file = rmakers.helpers.example(selections, divisions)
abjad.show(lilypond_file)
