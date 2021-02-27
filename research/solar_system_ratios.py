import abjad
import evans
from quicktions import Fraction

years = evans.Ratio(
    (
        248.59 * 365.26,
        164.79 * 365.26,
        84.01 * 365.26,
        29.46 * 365.26,
        11.86 * 365.26,
        1.88 * 365.26,
        365.26,
        224.7,
        87.97,
    )
).extract_sub_ratios(as_fractions=True)

days = [
    Fraction(24300, 100),
    Fraction(5860, 100),
    Fraction(639, 100),
    Fraction(103, 100),
    Fraction(99, 100),
    Fraction(72, 100),
    Fraction(67, 100),
    Fraction(45, 100),
    Fraction(41, 100),
]

years = evans.RatioClassSegment(years)

days = [Fraction(_, days[-1]) for _ in days]
days = evans.RatioClassSegment(days)

years = evans.Sequence(years).stack_pitches(as_ratios=True)

days = evans.Sequence(days).sort().stack_pitches(as_ratios=True)

for _ in years:
    print(_)

print("")

for _ in days:
    print(_)

staff1 = abjad.Staff([abjad.Note("fs,,4") for _ in years])

staff2 = abjad.Staff([abjad.Note("a,4") for _ in days])

h1 = evans.PitchHandler(years, as_ratios=True, forget=False)

h2 = evans.PitchHandler(days, as_ratios=True, forget=False)

h1(staff1)

abjad.attach(abjad.Clef("bass"), staff1[0])

abjad.attach(abjad.Clef("treble"), staff1[4])

abjad.attach(abjad.Clef("treble^8"), staff1[-2])

h2(staff2)

abjad.attach(abjad.Clef("bass"), staff2[0])

group = abjad.StaffGroup([staff1, staff2])

score = abjad.Score([group])

moment = "#(ly:make-moment 1 25)"
abjad.setting(score).proportional_notation_duration = moment

file = abjad.LilyPondFile(
    items=[
        score,
        abjad.Block(name="layout"),
    ],
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/ekmelos-ji-accidental-markups.ily",
    ],
)
file.layout_block.items.append(r'\accidentalStyle "dodecaphonic"')

abjad.show(file)
