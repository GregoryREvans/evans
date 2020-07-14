import abjad

durs = [abjad.Duration((5, 4)), abjad.Duration((1, 2))]
pitches = [1, 2]
signatures = [abjad.TimeSignature((3, 4)), abjad.TimeSignature((4, 4))]
skips = [abjad.Skip((1, 1), multiplier=abjad.Multiplier((_.pair))) for _ in signatures]
for sig, sk in zip(signatures, skips):
    abjad.attach(sig, sk)
sig_context = abjad.Staff(skips)
maker = abjad.LeafMaker()
selections = maker(pitches, durs)
staff = abjad.Staff([abjad.Voice(selections, name="Voice 1",),], name="Staff 1",)
staff_2 = abjad.Staff(
    [abjad.Voice(r"\times 4/5 {c'4 c'4 c'4 c'4 c'4} cs'2.", name="Voice 2",),],
    name="Staff 2",
)
score = abjad.Score([sig_context, staff_2, staff,], name="score",)
abjad.show(score)
for voice in abjad.select(score).components(abjad.Voice):
    selection = []
    for _ in voice:
        selection.append(_)
    selection = abjad.select(selection)
    shards = abjad.mutate(selection).split(signatures)
    v = abjad.Voice(name=voice.name)
    v.extend(shards)
    abjad.mutate(score[voice.name]).replace(v)
    shards_ = abjad.mutate(score[voice.name][:]).split(signatures)
    for i, shard_ in enumerate(shards_):
        abjad.Meter.rewrite_meter(shard_, signatures[i], rewrite_tuplets=False,)

abjad.show(score)
# print(abjad.lilypond(score))
