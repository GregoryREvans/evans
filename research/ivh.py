import abjad
import evans
from abjadext import rmakers

durations = [abjad.Duration(4, 4) for _ in range(5)]

stack1 = rmakers.stack(
    rmakers.talea([1, 2, 3, 2], 4, extra_counts=[0, 1, 0, -1]),
    rmakers.trivialize(abjad.select().tuplets()),
    rmakers.extract_trivial(abjad.select().tuplets()),
    rmakers.rewrite_rest_filled(abjad.select().tuplets()),
    rmakers.rewrite_sustained(abjad.select().tuplets()),
)

selections = stack1(durations)

voice = abjad.Voice(selections, name="Voice1")
staff = abjad.Staff([voice])

stack2 = rmakers.stack(
    rmakers.talea([1, 2, 3, 2], 8, extra_counts=[-1, 1, 0]),
    rmakers.trivialize(abjad.select().tuplets()),
    rmakers.extract_trivial(abjad.select().tuplets()),
    rmakers.rewrite_rest_filled(abjad.select().tuplets()),
    rmakers.rewrite_sustained(abjad.select().tuplets()),
)

rh = evans.RhythmHandler(stack2, forget=False)

ph1 = evans.PitchHandler([3, 2, 1, 0, -1, -2, -3, -2, -1, 0, 1, 1], forget=False)

ph1(voice)

ph2 = evans.PitchHandler([3, 4, 5, 4, 5, 6, 5, 6, 7, 6, 7, 6, 5, 4, 3, 4], forget=False)

ch = evans.CompositeHandler(rhythm_handler=rh, attachment_handlers=[ph2])

ivh = evans.IntermittentVoiceHandler(ch)

first = abjad.select(voice).leaves().get([0, 1, 2])

second = abjad.select(voice).leaves().get([6, 7])

third = abjad.select(voice).leaf(11)

ivh(first)

ivh(second)

ivh(third)

score = abjad.Score([staff])

file = abjad.LilyPondFile.new(
    score,
    includes=["/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"],
)

abjad.show(file)
