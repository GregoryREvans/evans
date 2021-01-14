import abjad
import evans
from abjadext import rmakers

nested_list = [1, [[1, [1, 1]], 1, [1, [1, 1, 1]], [1, [1, 1]], 1]]
# rtm = evans.nested_list_to_rtm(nested_list)
flat = evans.flatten(nested_list)

rtm = "(1 ((1 (2 3)) 4 (3 (2 1 2)) (3 (4 3)) 2))"
rotations = []
for i in range(len(evans.flatten(nested_list))):
    new_rtm = evans.rotate_tree(rtm, i)
    rotations.append(new_rtm)

funnels = []
for rotation in rotations:
    funnel = evans.funnel_inner_tree_to_x(rtm_string=rotation, x=6)
    funnels.append(funnel)

index_cycle = evans.cyc([i for i in range(len(funnels[0]))])
tuple_list = []
for i in range(len(rotations)):
    tuple_ = (i, next(index_cycle))
    tuple_list.append(tuple_)

final_rtm_list = []
for tuple_ in tuple_list:
    a = tuple_[0]
    b = tuple_[-1]
    final_rtm_list.append(funnels[a][b])

final_rtm_list = evans.Sequence(final_rtm_list).rotate(1)

for _ in final_rtm_list:
    print(_)

print(len(final_rtm_list))  # 13

durs = [
    (6, 4),
    (5, 4),
    (4, 4),
    (3, 4),
    (2, 4),
    (3, 4),
    (4, 4),
    (5, 4),
    (6, 4),
    (5, 4),
    (4, 4),
    (3, 4),
    (2, 4),
]

nonlast_tuplets = abjad.select().tuplets()[:-1]
last_leaf = abjad.select().leaf(-1)

s = rmakers.stack(
    evans.RTMMaker(final_rtm_list),
    rmakers.force_rest(abjad.select().leaves().get([0, -2, -1])),
    rmakers.tie(nonlast_tuplets.map(last_leaf)),
    rmakers.trivialize(abjad.select().tuplets()),
    rmakers.extract_trivial(abjad.select().tuplets()),
    rmakers.rewrite_rest_filled(abjad.select().tuplets()),
    rmakers.rewrite_sustained(abjad.select().tuplets()),
    rmakers.beam(),
)
h = evans.RhythmHandler(s, forget=False)
voice_1_selections = h(durs)
staff_1 = abjad.Staff(name="Voice 1", lilypond_type="RhythmicStaff")
staff_1.extend(voice_1_selections)


quantizer = evans.RhythmTreeQuantizer()
final_rtm_list = [quantizer(_) for _ in final_rtm_list]

print("")

for _ in final_rtm_list:
    print(_)

s = rmakers.stack(
    evans.RTMMaker(final_rtm_list),
    rmakers.force_rest(abjad.select().logical_ties().get([0, -2, -1])),
    rmakers.tie(nonlast_tuplets.map(last_leaf)),
    rmakers.trivialize(abjad.select().tuplets()),
    rmakers.extract_trivial(abjad.select().tuplets()),
    rmakers.rewrite_rest_filled(abjad.select().tuplets()),
    rmakers.rewrite_sustained(abjad.select().tuplets()),
    rmakers.beam(),
)
h = evans.RhythmHandler(s, forget=False)
voice_2_selections = h(durs)
staff_2 = abjad.Staff(name="Voice 2", lilypond_type="RhythmicStaff")
staff_2.extend(voice_2_selections)

global_context = abjad.Staff(name="Global Context", lilypond_type="GlobalContext")
for pair in durs:
    multiplier = abjad.Multiplier(pair)
    leaf = abjad.Skip((4, 4), multiplier=pair)
    sig = abjad.TimeSignature(pair)
    abjad.attach(sig, leaf)
    global_context.append(leaf)

score = abjad.Score(
    [
        global_context,
        abjad.StaffGroup(
            [
                staff_1,
                staff_2,
            ],
            name="StaffGroup",
        ),
    ],
    name="score",
)

# brackets = evans.NoteheadBracketMaker()
# brackets(score)

file = abjad.LilyPondFile(
    items=[score],
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/rhythm-maker-docs.ily",
    ],
)

abjad.show(file)
